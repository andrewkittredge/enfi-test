"""Order-dependency metrics computed from recorded trials.

Notation: a question has K canonical options and was shown under P permutations,
each answered n times (samples). ``P_p(o)`` is the empirical probability that the
model selected canonical option ``o`` when shown permutation ``p``.

Option Dependency Score (ODS)
-----------------------------
ODS measures how much the *selection distribution over options* moves when only
the ordering changes::

    ODS = sum_o Var_p[ P_p(o) ]  /  (1 - 1/K)

The numerator is the total variance of the selection probabilities across
permutations. It is 0 when every permutation yields the same distribution
(perfect order invariance). Its maximum, 1 - 1/K, is reached when each
permutation deterministically selects an option and the options are chosen
equally often overall - i.e. the answer is fully determined by the ordering
(e.g. the model always picks "A"). Dividing by that maximum normalises the score
to [0, 1].

``P_p(o)`` is estimated two ways. The headline ``ods`` treats every trial as a
one-hot pick of its chosen option (averaged over samples), so it is the same
quantity for every backend and, with one sample per permutation, measures
disagreement between permutations. ``ods_probability`` instead uses the
option-letter probabilities a local model exposes; it measures how far the
whole distribution moves and is ``None`` when the backend gave none. The two are
not comparable: a soft distribution cannot reach the one-hot maximum.

Supporting metrics
------------------
* consistency        - share of trials agreeing with the modal (majority) answer
* accuracy           - share of trials that are correct (order-averaged accuracy)
* majority correct   - whether the permutation-majority vote is correct (a
                       classic mitigation: "PriDe"/self-consistency over orderings)
* position share     - how often each presented position (A, B, C, ...) is chosen;
                       uniform (1/K) under a balanced permutation set if unbiased
* recall by position - accuracy when the correct option sits at each position;
                       its std (RStd, Zheng et al. 2024) is another sensitivity index
"""

from collections import Counter, defaultdict
from dataclasses import asdict
from statistics import mean, pstdev
from typing import Any

from order_dependency.analysis.question_metrics import QuestionMetrics
from order_dependency.mcq import MCQ
from order_dependency.trial import Trial


def _share(count: int, total: int) -> float:
    """Divide safely.

    Args:
        count: Numerator.
        total: Denominator, possibly zero.

    Returns:
        ``count / total``, or 0.0 when ``total`` is zero.
    """
    return count / total if total else 0.0


def selection_matrix(trials: list[Trial], k: int, use_probabilities: bool = True) -> dict[int, list[float]]:
    """Estimate ``P_p(o)`` for every permutation that received at least one answer.

    Args:
        trials: Trials for a single question.
        k: Number of options.
        use_probabilities: Let a trial contribute its model probabilities when the
            backend exposed them (paper-style). ``False`` forces one-hot vectors.

    Returns:
        Permutation index -> list of length ``k`` giving ``P_p(o)`` for each canonical
        option. A trial contributes its model probabilities when allowed and present,
        otherwise a one-hot vector for the chosen option; samples under the same
        ordering are averaged. Unanswered trials are ignored; permutations with no
        answers are absent.
    """
    by_perm: dict[int, list[list[float]]] = defaultdict(list)
    for t in trials:
        if t.canonical is None:
            continue
        distribution = [0.0] * k
        if use_probabilities and t.probabilities:
            for position, p in enumerate(t.probabilities):
                distribution[t.perm[position]] = p
        else:
            distribution[t.canonical] = 1.0
        by_perm[t.perm_index].append(distribution)
    return {p: [mean(d[o] for d in dists) for o in range(k)] for p, dists in by_perm.items()}


def ods_from_matrix(matrix: dict[int, list[float]], k: int) -> float:
    """Compute the Option Dependency Score from a selection matrix.

    Args:
        matrix: Output of ``selection_matrix``.
        k: Number of options.

    Returns:
        ``sum_o Var_p[P_p(o)] / (1 - 1/k)`` in ``[0, 1]``. Returns 0.0 when fewer
        than two permutations were answered (no variance can be measured) or
        ``k < 2``.
    """
    if len(matrix) < 2 or k < 2:
        return 0.0
    total_var = sum(pstdev(row[o] for row in matrix.values()) ** 2 for o in range(k))
    return total_var / (1 - 1 / k)


def _permutation_rows(mcq: MCQ, answered: list[Trial], matrix: dict[int, list[float]]) -> list[dict[str, Any]]:
    """Summarise each ordering for the report's discrepancy table.

    Args:
        mcq: The question.
        answered: Answered trials for ``mcq``.
        matrix: Output of ``selection_matrix``.

    Returns:
        One dict per ordering (sorted by permutation index) with the presented
        order, where the correct option sat, the modal answer and its distribution.
    """
    rows = []
    for p in sorted(matrix):
        picks = [t for t in answered if t.perm_index == p]
        perm = picks[0].perm
        modal = Counter(t.canonical for t in picks).most_common(1)[0][0]
        rows.append({
            "perm_index": p,
            "perm": list(perm),
            "presented_order": [mcq.display[i] for i in perm],
            "correct_position": perm.index(mcq.answer),
            "modal_canonical": modal,
            "modal_text": mcq.display[modal],
            "modal_correct": modal == mcq.answer,
            "distribution": matrix[p],
        })
    return rows


def question_metrics(mcq: MCQ, trials: list[Trial]) -> QuestionMetrics:
    """Compute all per-question metrics.

    Args:
        mcq: The question.
        trials: Every trial recorded for ``mcq`` (any ordering, any sample).

    Returns:
        The populated ``QuestionMetrics``. Shares and ODS are computed over
        *answered* trials only; ``n_trials`` vs ``n_answered`` exposes the gap.
    """
    answered = [t for t in trials if t.canonical is not None]
    n = len(answered)
    matrix = selection_matrix(trials, mcq.k)
    onehot = selection_matrix(trials, mcq.k, use_probabilities=False)
    has_probabilities = any(t.probabilities for t in answered)
    canon_counts = Counter(t.canonical for t in answered)
    pos_counts = Counter(t.position for t in answered)
    majority = canon_counts.most_common(1)[0][0] if canon_counts else None

    return QuestionMetrics(
        question_id=mcq.id,
        k=mcq.k,
        n_permutations=len({t.perm_index for t in trials}),
        n_trials=len(trials),
        n_answered=n,
        ods=ods_from_matrix(onehot, mcq.k),
        ods_probability=ods_from_matrix(matrix, mcq.k) if has_probabilities else None,
        consistency=_share(canon_counts[majority], n),
        accuracy=_share(sum(bool(t.correct) for t in answered), n),
        majority_canonical=majority,
        majority_correct=None if majority is None else majority == mcq.answer,
        answer_distribution={o: _share(canon_counts[o], n) for o in range(mcq.k)},
        position_share={j: _share(pos_counts[j], n) for j in range(mcq.k)},
        per_permutation_answers=_permutation_rows(mcq, answered, matrix),
    )


def recall_by_position(trials: list[Trial], mcqs_by_id: dict[str, MCQ]) -> dict[int, float]:
    """Compute accuracy conditioned on where the correct option was displayed.

    Args:
        trials: Trials across all questions.
        mcqs_by_id: Lookup from question id to ``MCQ`` (needed for the answer index).

    Returns:
        Presented position -> accuracy of answered trials whose correct option sat
        at that position, sorted by position. Positions never hosting a correct
        option are absent.
    """
    hits: dict[int, list[bool]] = defaultdict(list)
    for t in trials:
        if t.canonical is not None:
            hits[t.perm.index(mcqs_by_id[t.question_id].answer)].append(bool(t.correct))
    return {pos: mean(v) for pos, v in sorted(hits.items())}


def aggregate(mcqs: list[MCQ], trials: list[Trial]) -> dict[str, Any]:
    """Compute per-question metrics plus dataset-level summaries.

    Args:
        mcqs: All questions in the run (questions without trials are skipped).
        trials: All recorded trials.

    Returns:
        A JSON-serialisable dict with counts (``n_questions``, ``n_trials``,
        ``n_answered``, ``n_unanswered``, ``n_errors``), an ``error_summary`` of the
        five most common error messages, one-hot ODS statistics (``mean_ods``,
        ``median_ods``, ``max_ods``), ``mean_ods_probability`` (``None`` unless the
        backend exposed option probabilities), ``questions_with_disagreement``,
        ``mean_consistency``, ``trial_accuracy``, ``original_accuracy`` (accuracy on
        the as-authored ordering only), ``majority_vote_accuracy``,
        ``position_share``, ``recall_by_position``, ``recall_std``, token totals,
        and ``per_question`` (each ``QuestionMetrics`` as a dict).
    """
    by_q: dict[str, list[Trial]] = defaultdict(list)
    for t in trials:
        by_q[t.question_id].append(t)
    per_question = [question_metrics(m, by_q[m.id]) for m in mcqs if by_q.get(m.id)]

    answered = [t for t in trials if t.canonical is not None]
    n = len(answered)
    pos_counts = Counter(t.position for t in answered)
    recall = recall_by_position(trials, {m.id: m for m in mcqs})
    original = [t for t in answered if list(t.perm) == sorted(t.perm)]  # identity ordering = as authored
    ods_values = sorted(q.ods for q in per_question)
    ods_probability = [q.ods_probability for q in per_question if q.ods_probability is not None]
    errors = Counter(t.error for t in trials if t.error)
    return {
        "n_questions": len(per_question),
        "n_trials": len(trials),
        "n_answered": n,
        "n_unanswered": len(trials) - n,
        "n_errors": sum(errors.values()),
        "error_summary": dict(errors.most_common(5)),
        "mean_ods": mean(ods_values) if ods_values else 0.0,
        "median_ods": ods_values[len(ods_values) // 2] if ods_values else 0.0,
        "max_ods": max(ods_values, default=0.0),
        "mean_ods_probability": mean(ods_probability) if ods_probability else None,
        # A question with no answers has consistency 0.0 but is not a disagreement.
        "questions_with_disagreement": sum(q.n_answered > 0 and q.consistency < 1.0 for q in per_question),
        "mean_consistency": mean(q.consistency for q in per_question) if per_question else 0.0,
        "trial_accuracy": _share(sum(bool(t.correct) for t in answered), n),
        "original_accuracy": _share(sum(bool(t.correct) for t in original), len(original)),
        "majority_vote_accuracy": _share(sum(bool(q.majority_correct) for q in per_question), len(per_question)),
        "position_share": {j: _share(pos_counts[j], n) for j in range(max(m.k for m in mcqs))},
        "recall_by_position": recall,
        "recall_std": pstdev(recall.values()) if len(recall) > 1 else 0.0,
        "total_input_tokens": sum(t.input_tokens for t in trials),
        "total_output_tokens": sum(t.output_tokens for t in trials),
        "per_question": [asdict(q) for q in per_question],
    }

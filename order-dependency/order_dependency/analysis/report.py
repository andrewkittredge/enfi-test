"""Write the structured report: results.json, trials.csv and report.md."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd

from order_dependency.analysis.metrics import aggregate
from order_dependency.mcq import MCQ
from order_dependency.prompt import LABELS
from order_dependency.runner.experiment_run import ExperimentRun
from order_dependency.trial import Trial

Summary = dict[str, Any]


def write_report(run: ExperimentRun, out_dir: str | Path) -> Summary:
    """Compute metrics for a run and write all output files.

    Args:
        run: A completed run, fresh from ``runner.run_experiment`` or rebuilt from a
            previous ``results.json`` with ``ExperimentRun.model_validate_json``.
        out_dir: Directory to write into; created if missing.

    Returns:
        The summary dict from ``metrics.aggregate``. Side effects: writes
        ``results.json`` (run + summary), ``trials.csv`` and ``report.md``.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary = aggregate(run.questions, run.trials)
    (out / "results.json").write_text(
        json.dumps({**run.model_dump(), "summary": summary}, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    _write_csv(run.trials, run.questions, out / "trials.csv")
    (out / "report.md").write_text(render_markdown(run, summary), encoding="utf-8")
    return summary


def _write_csv(trials: list[Trial], mcqs: list[MCQ], path: Path) -> None:
    """Write one row per trial with letters and option texts resolved for humans.

    Args:
        trials: All trials in the run.
        mcqs: The questions, used to resolve indices to option text.
        path: Destination file.
    """
    by_id = {m.id: m for m in mcqs}
    df = pd.DataFrame([asdict(t) for t in trials])
    mcq = df["question_id"].map(by_id)
    df["presented_order"] = [" | ".join(m.display[i] for i in perm) for m, perm in zip(mcq, df["perm"])]
    df["correct_label"] = [LABELS[perm.index(m.answer)] for m, perm in zip(mcq, df["perm"])]
    df["chosen_label"] = df["position"].map(lambda p: LABELS[int(p)], na_action="ignore")
    # Unanswered trials arrive as NaN (pandas promotes None in an int column to float).
    df["chosen_option"] = [None if pd.isna(c) else m.display[int(c)] for m, c in zip(mcq, df["canonical"])]
    columns = [
        "question_id",
        "perm_index",
        "presented_order",
        "correct_label",
        "sample",
        "chosen_label",
        "chosen_option",
        "correct",
        "stop_reason",
        "input_tokens",
        "output_tokens",
        "latency_s",
        "raw_text",
        "error",
    ]
    df[columns].to_csv(path, index=False, encoding="utf-8")


def _pct(x: float) -> str:
    """Format a share as a percentage.

    Args:
        x: A value in ``[0, 1]``.

    Returns:
        E.g. ``"37.5%"``.
    """
    return f"{100 * x:.1f}%"


def _header(run: ExperimentRun, s: Summary) -> list[str]:
    """Run configuration and request counts.

    Args:
        run: The completed run.
        s: The summary.

    Returns:
        Markdown lines.
    """
    cfg = run.config
    if cfg.backend == "hf":
        precision = cfg.quantize or "fp16"
        settings = f"local Hugging Face model, {precision}, scored from option-letter logits"
    else:
        settings = f"thinking: `{cfg.thinking}` · effort: `{cfg.effort}` · max_tokens: {cfg.max_tokens}"
    lines = [
        "# Order dependency report",
        "",
        f"- Run at: {run.run_at}",
        f"- Model: `{cfg.model}` · {settings}",
        f"- Permutation strategy: `{run.strategy}` · samples per ordering: {run.samples}",
        f"- Prompts: {s['n_trials']} ({s['n_unanswered']} unanswered/unparseable) · "
        f"tokens in/out: {s['total_input_tokens']:,}/{s['total_output_tokens']:,}",
    ]
    if s["n_errors"]:
        lines.append(f"- **{s['n_errors']} requests failed.** Most common errors:")
        lines += [f"  - {n}× `{msg[:200]}`" for msg, n in s["error_summary"].items()]
    return lines + [""]


def _headline(s: Summary) -> list[str]:
    """Dataset-level metrics table.

    Args:
        s: The summary.

    Returns:
        Markdown lines.
    """
    probability_row = []
    if s["mean_ods_probability"] is not None:
        probability_row = [f"| Mean ODS from option-letter probabilities | {s['mean_ods_probability']:.3f} |"]
    return [
        "## Headline metrics",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Mean ODS (0 = order-invariant, 1 = fully order-determined) | **{s['mean_ods']:.3f}** |",
        f"| Median / max ODS | {s['median_ods']:.3f} / {s['max_ods']:.3f} |",
        *probability_row,
        f"| Questions with at least one order-induced answer change | "
        f"{s['questions_with_disagreement']} / {s['n_questions']} |",
        f"| Mean consistency (agreement with modal answer) | {_pct(s['mean_consistency'])} |",
        f"| Accuracy per prompt (averaged over orderings) | {_pct(s['trial_accuracy'])} |",
        f"| Accuracy of permutation majority vote (mitigation) | {_pct(s['majority_vote_accuracy'])} |",
        f"| Recall std across correct-answer positions (RStd) | {s['recall_std']:.3f} |",
        "",
    ]


def _answer_moving(s: Summary, k: int) -> list[str]:
    """Accuracy on the original ordering vs. with the gold answer moved to each position.

    Mirrors Table 1 of Zheng et al. (2024): each moved-to-X column is the recall of
    position X, shown with its delta from the original-order accuracy.

    Args:
        s: The summary.
        k: Largest option count in the dataset.

    Returns:
        Markdown lines.
    """
    orig = s["original_accuracy"]
    moved = " | ".join(
        f"{_pct(r)} ({100 * (r - orig):+.1f})" for r in (s["recall_by_position"].get(j, 0.0) for j in range(k))
    )
    return [
        "## Answer-moving attack (paper Table 1)",
        "",
        "Accuracy on the options as authored (Orig), and accuracy when every question's correct option "
        "is moved to a fixed position; parentheses give the change in points versus Orig.",
        "",
        "| Orig | " + " | ".join(f"Move gold to {c}" for c in LABELS[:k]) + " |",
        "|---|" + "---|" * k,
        f"| {_pct(orig)} | {moved} |",
        "",
    ]


def _position_bias(s: Summary, k: int) -> list[str]:
    """Letters chosen vs. where the correct option sat.

    Args:
        s: The summary.
        k: Largest option count in the dataset.

    Returns:
        Markdown lines.
    """
    share = " | ".join(_pct(s["position_share"].get(j, 0.0)) for j in range(k))
    recall = " | ".join(_pct(s["recall_by_position"].get(j, 0.0)) for j in range(k))
    return [
        "## Position bias",
        "",
        "Share of answers landing on each displayed position, and accuracy when the correct option "
        "was displayed at that position (for extraction items, position A is the first line of the "
        f"excerpt). A balanced permutation set should give a uniform share (~{_pct(1 / k)}) and flat "
        "recall if the model ignores ordering.",
        "",
        "| Position | " + " | ".join(LABELS[:k]) + " |",
        "|---|" + "---|" * k,
        f"| Chosen share | {share} |",
        f"| Recall when correct is here | {recall} |",
        "",
    ]


def _per_question(s: Summary, by_id: dict[str, MCQ]) -> list[str]:
    """Per-question table, most order-sensitive first.

    Args:
        s: The summary.
        by_id: Question lookup.

    Returns:
        Markdown lines.
    """
    lines = [
        "## Per-question results",
        "",
        "| ID | Topic | Difficulty | ODS | Consistency | Accuracy | Majority answer | Majority correct |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for q in sorted(s["per_question"], key=lambda q: -q["ods"]):
        m = by_id[q["question_id"]]
        maj = "-" if q["majority_canonical"] is None else m.display[q["majority_canonical"]]
        lines.append(
            f"| {m.id} | {m.topic} | {m.difficulty} | {q['ods']:.3f} | {_pct(q['consistency'])} | "
            f"{_pct(q['accuracy'])} | {maj} | {'yes' if q['majority_correct'] else 'no'} |"
        )
    return lines + [""]


def _discrepancies(s: Summary, by_id: dict[str, MCQ]) -> list[str]:
    """The demonstrative part: every question whose answer changed with ordering, ordering by ordering.

    Args:
        s: The summary.
        by_id: Question lookup.

    Returns:
        Markdown lines.
    """
    lines = ["## Discrepancies: same question, different orderings, different answers", ""]
    flagged = [q for q in s["per_question"] if q["n_answered"] > 0 and q["consistency"] < 1.0]
    if not flagged:
        lines.append("None - every question received the same answer under every ordering.")
    for q in sorted(flagged, key=lambda q: -q["ods"]):
        m = by_id[q["question_id"]]
        lines += [
            f"### {m.id} - {m.question}",
            "",
            f"Correct: **{m.correct_text}**. Options: " + "; ".join(m.display),
            "",
            "| Ordering (A, B, ...) | Correct at | Answer | Correct? |",
            "|---|---|---|---|",
        ]
        for pp in q["per_permutation_answers"]:
            order = ", ".join(f"{LABELS[j]}={o}" for j, o in enumerate(pp["presented_order"]))
            lines.append(
                f"| {order} | {LABELS[pp['correct_position']]} | {pp['modal_text']} | "
                f"{'yes' if pp['modal_correct'] else 'no'} |"
            )
        lines.append("")
    return lines


def _questions_used(mcqs: list[MCQ]) -> list[str]:
    """The question set with correct answers marked.

    Args:
        mcqs: The questions.

    Returns:
        Markdown lines.
    """
    lines = ["## Questions used", ""]
    for m in mcqs:
        lines.append(f"- **{m.id}** ({m.topic}, {m.difficulty}): {m.question}")
        lines += [f"  - {o}{'  ✅' if i == m.answer else ''}" for i, o in enumerate(m.options)]
        if m.is_extraction:
            lines.append("  - values: " + "; ".join(m.values))
    return lines + [""]


def render_markdown(run: ExperimentRun, s: Summary) -> str:
    """Render the human-readable report.

    Args:
        run: The completed run.
        s: The summary dict from ``metrics.aggregate``.

    Returns:
        The report as a Markdown string.
    """
    by_id = {m.id: m for m in run.questions}
    k = max(m.k for m in run.questions)
    return "\n".join(
        _header(run, s)
        + _headline(s)
        + _answer_moving(s, k)
        + _position_bias(s, k)
        + _per_question(s, by_id)
        + _discrepancies(s, by_id)
        + _questions_used(run.questions)
    )

"""Tests for ODS and the aggregate metrics, using synthetic answerers."""

import itertools
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from order_dependency.analysis.metrics import aggregate, ods_from_matrix, question_metrics, selection_matrix
from order_dependency.analysis.report import write_report
from order_dependency.mcq import MCQ
from order_dependency.runner.experiment_run import ExperimentRun
from order_dependency.runner.llm_config import LLMConfig
from order_dependency.strategy import Strategy
from order_dependency.trial import Trial

# Four options, correct answer at canonical index 1.
MCQ4 = MCQ("q", "?", ("a", "b", "c", "d"), answer=1)


def make_trials(mcq: MCQ, choose_position) -> list[Trial]:
    """Simulate an answerer over every full permutation of ``mcq``.

    Args:
        mcq: The question.
        choose_position: Callable ``perm -> presented position`` standing in for the model.

    Returns:
        One answered ``Trial`` per permutation.
    """
    trials = []
    for i, perm in enumerate(itertools.permutations(range(mcq.k))):
        pos = choose_position(perm)
        canon = perm[pos]
        trials.append(Trial(mcq.id, i, perm, 0, pos, canon, canon == mcq.answer, "", "end_turn", 0, 0, 0.0))
    return trials


class OdsTests(unittest.TestCase):
    """ODS must hit its documented endpoints."""

    def test_invariant_model_has_zero_ods_and_full_consistency(self):
        """An answerer that always finds the correct option scores ODS 0."""
        q = question_metrics(MCQ4, make_trials(MCQ4, lambda perm: perm.index(1)))
        self.assertAlmostEqual(q.ods, 0.0)
        self.assertEqual(q.consistency, 1.0)
        self.assertEqual(q.accuracy, 1.0)
        self.assertIs(q.majority_correct, True)

    def test_always_pick_A_is_maximally_order_dependent(self):
        """An answerer that always picks position A scores ODS 1 and 25% accuracy."""
        q = question_metrics(MCQ4, make_trials(MCQ4, lambda perm: 0))
        self.assertAlmostEqual(q.ods, 1.0)
        self.assertAlmostEqual(q.accuracy, 0.25)
        self.assertEqual(q.position_share[0], 1.0)

    def test_two_options_with_disjoint_picks_give_max_ods(self):
        """Two orderings, two disjoint one-hot picks over K=2: variance 0.25*2 / (1-1/2) = 1."""
        self.assertAlmostEqual(ods_from_matrix({0: [1, 0], 1: [0, 1]}, 2), 1.0)

    def test_trial_probabilities_feed_the_selection_matrix(self):
        """When trials carry logit probabilities, P_p(o) is the probability mapped to canonical options."""
        perm = (2, 0, 1, 3)  # position A shows canonical option 2, B shows 0, ...
        trial = Trial("q", 0, perm, 0, 1, 0, False, "B", "logits", 0, 0, 0.0, probabilities=(0.1, 0.6, 0.2, 0.1))
        matrix = selection_matrix([trial], 4)
        self.assertEqual(matrix, {0: [0.6, 0.2, 0.1, 0.1]})

    def test_probability_trials_give_one_hot_ods_and_a_probability_ods(self):
        """The headline ODS ignores probabilities; ``ods_probability`` uses them."""
        probs = [(0.6, 0.2, 0.1, 0.1), (0.5, 0.3, 0.1, 0.1)]
        trials = []
        for i, perm in enumerate([(0, 1, 2, 3), (1, 0, 2, 3)]):
            canon = perm[0]  # argmax is position A under both orderings, so a different canonical option each time
            trial = Trial("q", i, perm, 0, 0, canon, canon == 1, "A", "logits", 0, 0, 0.0, probabilities=probs[i])
            trials.append(trial)
        q = question_metrics(MCQ4, trials)
        self.assertAlmostEqual(q.ods, (0.25 + 0.25) / (1 - 1 / 4))  # two options with variance 0.25 each
        self.assertAlmostEqual(q.ods_probability, ods_from_matrix(selection_matrix(trials, 4), 4))
        self.assertLess(q.ods_probability, q.ods)

    def test_sampled_trials_have_no_probability_ods(self):
        """API trials carry no probabilities, so only the one-hot ODS is defined."""
        q = question_metrics(MCQ4, make_trials(MCQ4, lambda perm: 0))
        self.assertIsNone(q.ods_probability)

    def test_soft_probabilities_reduce_ods(self):
        """A stable modal answer with mild probability wobble yields a small positive ODS."""
        ods = ods_from_matrix({0: [0.9, 0.1, 0, 0], 1: [0.8, 0.2, 0, 0]}, 4)
        self.assertGreater(ods, 0)
        self.assertLess(ods, 0.05)


class ExperimentRunTests(unittest.TestCase):
    """The run record must build from the runner's arguments and survive a JSON round trip."""

    def test_round_trip(self):
        """model_dump -> JSON -> model_validate_json reproduces the run, tuples included."""
        run = ExperimentRun(
            config=LLMConfig(), strategy=Strategy.FULL, samples=1, n_random=None, seed=0,
            questions=[MCQ4], trials=make_trials(MCQ4, lambda perm: 0),
        )
        loaded = ExperimentRun.model_validate_json(json.dumps(run.model_dump()))
        self.assertEqual(loaded, run)
        self.assertIsInstance(loaded.trials[0].perm, tuple)

    def test_report_with_unanswered_trial(self):
        """A refused prompt (no position/canonical) still produces the CSV and Markdown report."""
        trials = make_trials(MCQ4, lambda perm: perm.index(1))
        trials[0] = Trial(MCQ4.id, 0, trials[0].perm, 0, None, None, None, "", "refusal", 0, 0, 0.0)
        run = ExperimentRun(
            config=LLMConfig(), strategy=Strategy.FULL, samples=1, n_random=None, seed=0,
            questions=[MCQ4], trials=trials,
        )
        with tempfile.TemporaryDirectory() as out:
            summary = write_report(run, out)
            csv = pd.read_csv(Path(out) / "trials.csv")
        self.assertEqual(summary["n_unanswered"], 1)
        self.assertTrue(pd.isna(csv.loc[0, "chosen_option"]))
        self.assertEqual(csv.loc[1, "chosen_option"], "b")


class AggregateTests(unittest.TestCase):
    """Dataset-level summaries."""

    def test_aggregate_majority_vote_and_position_recall(self):
        """An always-A answerer is only right when the answer is shown first."""
        agg = aggregate([MCQ4], make_trials(MCQ4, lambda perm: 0))
        self.assertAlmostEqual(agg["mean_ods"], 1.0)
        self.assertEqual(agg["position_share"][0], 1.0)
        self.assertEqual(agg["recall_by_position"], {0: 1.0, 1: 0.0, 2: 0.0, 3: 0.0})
        self.assertEqual(agg["original_accuracy"], 0.0)  # as authored, the answer sits at B
        self.assertGreater(agg["recall_std"], 0.4)
        self.assertEqual(agg["questions_with_disagreement"], 1)


if __name__ == "__main__":
    unittest.main()

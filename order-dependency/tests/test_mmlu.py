"""Tests for converting MMLU rows into MCQs (no network: a synthetic frame stands in for the parquet)."""

import unittest
from collections import Counter

import pandas as pd

from order_dependency.mmlu import to_mcqs


def _frame() -> pd.DataFrame:
    """Five MMLU-shaped rows over two subjects.

    Returns:
        A frame with the ``cais/mmlu`` columns.
    """
    abcd, wxyz = ["a", "b", "c", "d"], ["w", "x", "y", "z"]
    physics = [{"subject": "physics", "question": f"p{i}", "choices": abcd, "answer": i} for i in range(3)]
    art = [{"subject": "art", "question": f"a{i}", "choices": wxyz, "answer": 0} for i in range(2)]
    return pd.DataFrame(physics + art)


class ToMcqsTests(unittest.TestCase):
    """``to_mcqs`` maps rows to ``MCQ`` objects and samples per subject."""

    def test_all_rows_become_mcqs_grouped_by_subject(self):
        """Without a cap every row is kept, ordered by subject, with the row index in the id."""
        mcqs = to_mcqs(_frame(), None, 0)
        self.assertEqual([m.topic for m in mcqs], ["art", "art", "physics", "physics", "physics"])
        self.assertEqual(mcqs[2].id, "mmlu-physics-0")
        self.assertEqual(mcqs[2].options, ("a", "b", "c", "d"))
        self.assertEqual(mcqs[3].answer, 1)

    def test_per_subject_caps_each_subject_and_is_seeded(self):
        """A cap keeps at most that many questions per subject and the same seed gives the same draw."""
        first = to_mcqs(_frame(), 2, 0)
        again = to_mcqs(_frame(), 2, 0)
        self.assertEqual(Counter(m.topic for m in first), {"art": 2, "physics": 2})
        self.assertEqual(first, again)

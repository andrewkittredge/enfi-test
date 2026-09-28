"""Order-dependency metrics for a single question."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QuestionMetrics:
    """Everything the report needs to say about one question.

    Attributes:
        question_id: Id of the ``MCQ`` these metrics describe.
        k: Number of options.
        n_permutations: Distinct orderings that were asked.
        n_trials: Total prompts sent for this question.
        n_answered: Prompts that yielded a parseable letter.
        ods: Option Dependency Score in ``[0, 1]`` from one-hot picks, comparable across
            backends (see ``metrics`` module docstring).
        ods_probability: ODS from the model's option-letter probabilities, or ``None``
            when the backend did not expose them.
        consistency: Share of answered trials agreeing with the modal option.
        accuracy: Share of answered trials that chose the correct option.
        majority_canonical: The modal canonical option, or ``None`` if nothing was answered.
        majority_correct: Whether the modal option is correct, or ``None`` if nothing was answered.
        answer_distribution: Canonical option -> share of answered trials choosing it.
        position_share: Presented position -> share of answered trials choosing it.
        per_permutation_answers: One dict per ordering with the presented order, where
            the correct option sat, the modal answer, and the selection distribution.
    """

    question_id: str
    k: int
    n_permutations: int
    n_trials: int
    n_answered: int
    ods: float
    ods_probability: float | None
    consistency: float
    accuracy: float
    majority_canonical: int | None
    majority_correct: bool | None
    answer_distribution: dict[int, float]
    position_share: dict[int, float]
    per_permutation_answers: list[dict[str, Any]] = field(default_factory=list)

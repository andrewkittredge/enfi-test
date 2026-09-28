"""Names of the option-reordering strategies."""

from enum import StrEnum


class Strategy(StrEnum):
    """How the answer options of a question are reordered across prompts.

    Attributes:
        FULL: All ``k!`` orderings (exact ODS; 24 for k=4, 120 for k=5).
        CYCLIC: The ``k`` rotations; every option visits every position once.
        PLACE_CORRECT: The correct option at each position, distractors in fixed order
            (the "answer-moving attack" of Zheng et al. 2024).
        RANDOM: A seeded sample of ``n`` distinct orderings.
    """

    FULL = "full"
    CYCLIC = "cyclic"
    PLACE_CORRECT = "place-correct"
    RANDOM = "random"

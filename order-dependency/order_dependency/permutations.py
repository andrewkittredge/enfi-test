"""Generate option orderings for a question under a ``Strategy``.

A permutation is a tuple ``perm`` of canonical option indices where ``perm[j]``
is the canonical option shown at presented position ``j`` (position 0 = "A").
"""

import itertools
import random

from order_dependency.strategy import Strategy

Permutation = tuple[int, ...]


def place_correct(k: int, answer: int) -> list[Permutation]:
    """Move only the correct option through every position; distractors keep their order.

    Isolates pure *position* bias from effects caused by which distractors sit
    next to each other.

    Args:
        k: Number of options.
        answer: Canonical index of the correct option.

    Returns:
        ``k`` permutations, the ``p``-th showing the correct option at position ``p``.
    """
    others = [i for i in range(k) if i != answer]
    perms = []
    for pos in range(k):
        order = others[:pos] + [answer] + others[pos:]
        perms.append(tuple(order))
    return perms


def generate(strategy: Strategy, k: int, answer: int, n: int | None = None, seed: int = 0) -> list[Permutation]:
    """Produce the orderings for one question under a strategy.

    Args:
        strategy: The reordering strategy.
        k: Number of options.
        answer: Canonical index of the correct option (used by ``PLACE_CORRECT``).
        n: Orderings per question for ``RANDOM``; defaults to ``k``. Ignored otherwise.
        seed: Seed for ``RANDOM``. Ignored otherwise.

    Returns:
        The permutations produced by the chosen strategy.
    """
    identity = tuple(range(k))
    everything = list(itertools.permutations(identity))
    match strategy:
        case Strategy.FULL:
            return everything
        case Strategy.CYCLIC:
            return [identity[shift:] + identity[:shift] for shift in range(k)]
        case Strategy.PLACE_CORRECT:
            return place_correct(k, answer)
        case Strategy.RANDOM:
            rng = random.Random(seed)
            count = min(n or k, len(everything))
            return rng.sample(everything, count)


def to_canonical(perm: Permutation, position: int) -> int:
    """Map a presented position back to the canonical option it displayed.

    Args:
        perm: Permutation that was shown.
        position: Presented position chosen by the model (0 = "A").

    Returns:
        The canonical option index shown at that position.
    """
    return perm[position]

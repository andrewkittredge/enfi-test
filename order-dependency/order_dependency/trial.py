"""One answered prompt: a question shown under one ordering, answered once."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Trial:
    """The persisted record of a single prompt/answer pair.

    Unlike ``Answer`` (which only knows about letters), a trial knows which
    question and ordering were shown, so the letter is already resolved to a
    canonical option and a correctness flag.

    Attributes:
        question_id: Id of the ``MCQ`` that was asked.
        perm_index: Index of the ordering within the question's permutation list.
        perm: The ordering itself (canonical option at each presented position).
        sample: Sample number when the same ordering is asked more than once.
        position: Presented position chosen (0 = "A"), or ``None`` if unanswered.
        canonical: Canonical option chosen, or ``None`` if unanswered.
        correct: Whether the chosen option is the answer, or ``None`` if unanswered.
        raw_text: The model's reply verbatim.
        stop_reason: The API's ``stop_reason``, or ``None`` on transport error.
        input_tokens: Billed input tokens.
        output_tokens: Billed output tokens.
        latency_s: Wall-clock seconds for the request.
        error: Transport/API error description, else ``None``.
        probabilities: Model probability of each presented position (A, B, ...), when
            the backend exposes logits; ``None`` for sampled API answers.
    """

    question_id: str
    perm_index: int
    perm: tuple[int, ...]
    sample: int
    position: int | None
    canonical: int | None
    correct: bool | None
    raw_text: str
    stop_reason: str | None
    input_tokens: int
    output_tokens: int
    latency_s: float
    error: str | None = None
    probabilities: tuple[float, ...] | None = None

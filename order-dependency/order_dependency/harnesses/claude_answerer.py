"""Ask Claude to answer one rendered MCQ."""

import asyncio
import time
from typing import TYPE_CHECKING

import anthropic

from order_dependency.mcq import MCQ
from order_dependency.permutations import Permutation, to_canonical
from order_dependency.prompt import build_prompt, parse_reply, system_prompt
from order_dependency.trial import Trial

if TYPE_CHECKING:  # llm_config imports this module, so the type is only needed statically
    from order_dependency.runner.llm_config import LLMConfig


class ClaudeAnswerer:
    """Thin async wrapper around the Anthropic Messages API with bounded concurrency.

    One API call per (question, permutation, sample). Refusals and max-token
    cut-offs are recorded as unanswered rather than retried on another model, so a
    run measures exactly one model.

    Attributes:
        config: Request settings shared by every call.
        client: The async Anthropic client. Credentials come from
            ``ANTHROPIC_API_KEY`` or an ``ant auth login`` profile.
    """

    def __init__(self, config: "LLMConfig", client: anthropic.AsyncAnthropic | None = None):
        """Create an answerer.

        Args:
            config: Request settings.
            client: Optional pre-built client (e.g. for tests); a default client with
                five retries on 429/5xx is created when omitted.
        """
        self.config = config
        self.client = client or anthropic.AsyncAnthropic(max_retries=5)
        self._sem = asyncio.Semaphore(config.concurrency)

    async def answer(self, mcq: MCQ, perm_index: int, perm: Permutation, sample: int) -> Trial:
        """Ask the model one question under one ordering and record the outcome.

        Args:
            mcq: The question.
            perm_index: Index of ``perm`` in the question's permutation list.
            perm: Ordering of the options to present.
            sample: Sample number for this ordering.

        Returns:
            The trial. API and connection failures are captured in ``Trial.error``
            rather than raised, so a single bad request does not abort a run.
        """
        response, error = None, None
        async with self._sem:  # cap in-flight requests to stay under rate limits
            start = time.perf_counter()  # inside the semaphore: measure the request, not the queue
            try:
                response = await self.client.messages.create(
                    system=system_prompt(mcq),
                    messages=[{"role": "user", "content": build_prompt(mcq, perm)}],
                    **self.config.request_kwargs(),
                )
            except anthropic.APIStatusError as e:  # 4xx, or 5xx after the SDK's retries
                error = f"{e.status_code}: {e.message}"
            except anthropic.APIConnectionError as e:
                error = f"connection: {e}"

        text = "".join(b.text for b in response.content if b.type == "text") if response else ""
        # Only a naturally finished turn counts: a refusal or a max_tokens cut-off means
        # the model never committed to an answer.
        finished = response is not None and response.stop_reason == "end_turn"
        position = parse_reply(mcq, perm, text) if finished else None
        canonical = None if position is None else to_canonical(perm, position)
        correct = None if canonical is None else canonical == mcq.answer
        return Trial(
            question_id=mcq.id,
            perm_index=perm_index,
            perm=perm,
            sample=sample,
            position=position,
            canonical=canonical,
            correct=correct,
            raw_text=text,
            stop_reason=response.stop_reason if response else None,
            input_tokens=response.usage.input_tokens if response else 0,
            output_tokens=response.usage.output_tokens if response else 0,
            latency_s=round(time.perf_counter() - start, 3),
            error=error,
        )

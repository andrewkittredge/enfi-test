"""A completed experiment: what was asked, how, and what came back."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field, computed_field

from order_dependency.mcq import MCQ
from order_dependency.runner.llm_config import LLMConfig
from order_dependency.strategy import Strategy
from order_dependency.trial import Trial


def _now() -> str:
    """Current UTC time as an ISO-8601 string with second precision."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class ExperimentRun(BaseModel):
    """Self-contained record of one ``experiment`` invocation.

    Because it carries the questions and every trial, a saved run can be re-scored
    offline after metric changes without touching the API. Serialise with
    ``model_dump()`` / ``model_dump_json()``; rebuild from ``results.json`` with
    ``model_validate_json()`` (extra keys such as ``summary`` are ignored, and JSON
    lists are coerced back to the tuples the dataclasses expect).

    Attributes:
        config: LLM request settings used for every prompt.
        strategy: Permutation strategy name.
        samples: Times each ordering was asked.
        n_random: Orderings per question for the ``random`` strategy, else ``None``.
        seed: Seed for the ``random`` strategy.
        questions: The MCQs asked.
        trials: One entry per prompt sent.
        run_at: UTC ISO timestamp of the run.
    """

    config: LLMConfig
    strategy: Strategy
    samples: int
    n_random: int | None
    seed: int
    questions: list[MCQ]
    trials: list[Trial]
    run_at: str = Field(default_factory=_now)

    @computed_field
    @property
    def request_kwargs(self) -> dict:
        """Exact Messages API parameters, recorded so a report is readable without the code."""
        return self.config.request_kwargs()

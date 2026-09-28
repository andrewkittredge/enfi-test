"""Orchestrate the experiment: every question x every permutation x every sample."""

import asyncio
import sys

from tqdm.asyncio import tqdm

from order_dependency.harnesses.claude_answerer import ClaudeAnswerer
from order_dependency.harnesses.hf_answerer import HFAnswerer
from order_dependency.mcq import MCQ
from order_dependency.permutations import Permutation, generate
from order_dependency.runner.experiment_run import ExperimentRun
from order_dependency.runner.llm_config import LLMConfig
from order_dependency.runner.preflight_error import PreflightError
from order_dependency.strategy import Strategy
from order_dependency.trial import Trial

# (question, permutation index, permutation, sample number)
Job = tuple[MCQ, int, Permutation, int]


def plan(mcqs: list[MCQ], strategy: Strategy, n_random: int | None, seed: int, samples: int) -> list[Job]:
    """Enumerate every prompt the run will send.

    Args:
        mcqs: Questions to ask.
        strategy: Permutation strategy.
        n_random: Orderings per question for the ``random`` strategy.
        seed: Seed for the ``random`` strategy.
        samples: Times each ordering is asked.

    Returns:
        Jobs in question -> ordering -> sample order.
    """
    return [
        (mcq, p, perm, s)
        for mcq in mcqs
        for p, perm in enumerate(generate(strategy, mcq.k, mcq.answer, n_random, seed))
        for s in range(samples)
    ]


async def _run(jobs: list[Job], answerer: HFAnswerer | ClaudeAnswerer) -> list[Trial]:
    """Execute jobs concurrently, probing with the first one before fanning out.

    A tqdm bar on stderr tracks completed prompts.

    Args:
        jobs: Output of ``plan``.
        answerer: The LLM wrapper to query.

    Returns:
        One ``Trial`` per job, in job order.

    Raises:
        PreflightError: If the first request fails, before any others are sent.
    """
    first = await answerer.answer(*jobs[0])
    if first.error:
        raise PreflightError(f"first request to {answerer.config.model} failed: {first.error}")
    answers = (answerer.answer(*job) for job in jobs[1:])
    rest = await tqdm.gather(*answers, initial=1, total=len(jobs), unit="prompt")
    return [first, *rest]


def run_experiment(
    mcqs: list[MCQ],
    config: LLMConfig,
    strategy: Strategy = Strategy.PLACE_CORRECT,
    samples: int = 1,
    n_random: int | None = None,
    seed: int = 0,
) -> ExperimentRun:
    """Run the full experiment.

    Args:
        mcqs: Questions to ask.
        config: LLM request settings.
        strategy: Permutation strategy name.
        samples: Times each ordering is asked.
        n_random: Orderings per question for the ``random`` strategy.
        seed: Seed for the ``random`` strategy.

    Returns:
        The completed run. Feed it to ``report.write_report`` to compute metrics.

    Raises:
        PreflightError: If the first request fails.
    """
    jobs = plan(mcqs, strategy, n_random, seed, samples)
    print(
        f"Running {len(jobs)} prompts against {config.model} "
        f"({config.backend}, strategy={strategy}, samples={samples})",
        file=sys.stderr,
    )
    trials = asyncio.run(_run(jobs, config.answerer))
    return ExperimentRun(
        config=config, strategy=strategy, samples=samples, n_random=n_random, seed=seed, questions=mcqs, trials=trials
    )

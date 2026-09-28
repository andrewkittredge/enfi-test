"""Command-line interface for the order-dependency experiment.

Examples:
    order-dependency experiment -o opus5-nothink --thinking disabled     # writes <repo>/results/opus5-nothink
    order-dependency experiment -q mmlu --per-subject 20 -o mmlu-subset  # MMLU from HF
    order-dependency preview    -q mmlu --per-subject 1 --strategy cyclic  # show prompts, no API calls
"""

import argparse
import sys
from pathlib import Path

from order_dependency.analysis.report import write_report
from order_dependency.mcq import MCQ, load_questions
from order_dependency.mmlu import load_mmlu
from order_dependency.permutations import generate
from order_dependency.prompt import build_prompt
from order_dependency.runner.llm_config import LLMConfig
from order_dependency.runner.preflight_error import PreflightError
from order_dependency.runner.run_experiment import run_experiment
from order_dependency.strategy import Strategy

# Anchored to the project so the CLI works from any working directory.
DEFAULT_QUESTIONS = Path(__file__).resolve().parents[1] / "data" / "questions.json"
RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def _add_common(p: argparse.ArgumentParser) -> None:
    """Attach the question/permutation options shared by ``experiment`` and ``preview``.

    Args:
        p: The sub-parser to extend.
    """
    p.add_argument(
        "-q",
        "--questions",
        default=DEFAULT_QUESTIONS,
        type=Path,
        help="MCQ JSON file, or `mmlu` to fetch the MMLU test split from Hugging Face (cached after the first run)",
    )
    p.add_argument(
        "--per-subject",
        type=int,
        default=None,
        help="with -q mmlu: questions per subject, drawn with --seed (default: all)",
    )
    p.add_argument(
        "--strategy",
        type=Strategy,
        choices=list(Strategy),
        default=Strategy.PLACE_CORRECT,
        help="how to reorder options (default: place-correct = gold option at each position; full = all k! orderings)",
    )
    p.add_argument("--n-random", type=int, default=None, help="orderings per question for --strategy random")
    p.add_argument("--seed", type=int, default=0)


def _load_questions(args: argparse.Namespace) -> list[MCQ]:
    """Load the questions named by ``-q``: a JSON file, or ``mmlu`` for the Hugging Face dataset.

    Args:
        args: Parsed arguments of ``experiment`` or ``preview``.

    Returns:
        The MCQs to ask.
    """
    if str(args.questions) == "mmlu":
        return load_mmlu(args.per_subject, args.seed)
    return load_questions(args.questions)


def _print_summary(summary: dict, out: Path) -> None:
    """Print the one-line headline result and where the report went.

    Args:
        summary: The dict from ``metrics.aggregate``.
        out: Directory the report files were written to.
    """
    print(
        f"\nMean ODS: {summary['mean_ods']:.3f}   "
        f"questions with order-induced changes: {summary['questions_with_disagreement']}/{summary['n_questions']}   "
        f"accuracy: {summary['trial_accuracy']:.1%} -> majority vote {summary['majority_vote_accuracy']:.1%}"
    )
    print(f"Report written to {out / 'report.md'} (plus results.json, trials.csv)")


def cmd_experiment(args: argparse.Namespace) -> int:
    """``experiment``: query the LLM under every ordering and write the report.

    Args:
        args: Parsed arguments for the ``experiment`` sub-command.

    Returns:
        Process exit code: 0 on success, 1 if the first request failed.
    """
    mcqs = _load_questions(args)
    config = LLMConfig(
        backend=args.backend,
        model=args.model,
        quantize=args.quantize,
        thinking=args.thinking,
        effort=None if args.effort == "none" else args.effort,
        max_tokens=args.max_tokens,
        concurrency=args.concurrency,
    )
    try:
        run = run_experiment(
            mcqs, config, strategy=args.strategy, samples=args.samples, n_random=args.n_random, seed=args.seed
        )
    except PreflightError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    out = RESULTS_DIR / args.out  # an absolute --out is kept as-is by pathlib
    summary = write_report(run, out)
    _print_summary(summary, out)
    return 0


def cmd_preview(args: argparse.Namespace) -> int:
    """``preview``: print the prompts that would be sent, without calling the API.

    Args:
        args: Parsed arguments for the ``preview`` sub-command.

    Returns:
        Process exit code (always 0).
    """
    mcqs = _load_questions(args)
    total = 0
    for mcq in mcqs:
        perms = generate(args.strategy, mcq.k, mcq.answer, args.n_random, args.seed)
        total += len(perms)
        print(f"=== {mcq.id}: {len(perms)} orderings ===")
        for perm in perms[: args.limit]:
            print(build_prompt(mcq, perm))
            print("---")
    print(f"{total} prompts per sample", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with the ``experiment`` and ``preview`` sub-commands.

    Returns:
        The configured parser; each sub-command sets ``func`` to its handler.
    """
    parser = argparse.ArgumentParser(
        prog="order-dependency", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    experiment = sub.add_parser("experiment", help="query the LLM under every ordering and write a report")
    _add_common(experiment)
    experiment.add_argument("-o", "--out", type=Path, default=Path("latest"),
                     help=f"run name or output directory; relative paths are placed under {RESULTS_DIR}")
    experiment.add_argument(
        "--backend",
        choices=["claude", "hf"],
        default="claude",
        help="claude = Anthropic API; hf = local Hugging Face model scored from option-letter logits "
        "(needs `uv sync --group hf`)",
    )
    experiment.add_argument(
        "--model", default="claude-opus-5", help="Anthropic model id, or HF repo id/path for --backend hf"
    )
    experiment.add_argument(
        "--quantize",
        choices=["8bit", "4bit"],
        default=None,
        help="--backend hf only: bitsandbytes quantisation (default fp16)",
    )
    experiment.add_argument(
        "--thinking",
        choices=["adaptive", "disabled", "omit"],
        default="adaptive",
        help="adaptive = model decides how much to think; disabled = answer directly; "
        "omit = don't send the parameter (for models without adaptive thinking)",
    )
    experiment.add_argument(
        "--effort",
        choices=["low", "medium", "high", "none"],
        default="low",
        help="output_config.effort; 'none' omits it (required for Haiku 4.5)",
    )
    experiment.add_argument("--max-tokens", type=int, default=4096)
    experiment.add_argument("--samples", type=int, default=1, help="answers per ordering (estimates P_p(o))")
    experiment.add_argument("--concurrency", type=int, default=8)
    experiment.set_defaults(func=cmd_experiment)

    preview = sub.add_parser("preview", help="print the prompts that would be sent (no API calls)")
    _add_common(preview)
    preview.add_argument("--limit", type=int, default=2, help="orderings to print per question")
    preview.set_defaults(func=cmd_preview)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``order-dependency`` console script.

    Args:
        argv: Arguments to parse; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code from the selected sub-command.
    """
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A take-home tech test (see `Take Home Tech Test.pdf`) on the *order dependency problem* in LLM
answers to multiple-choice questions. The deliverables are:

- **Part 1** – a ≤500-word written explanation (PDF/Word, not yet present).
- **Part 2** – the `order-dependency/` Python application, its README and results.
- **Part 3** – `use-of-generative-ai.md`, describing how generative AI was used (currently empty).

All code lives in `order-dependency/`; run every command below from that directory.

## Commands

```bash
uv sync --group hf                       # install deps into .venv; plain `uv sync` removes the optional torch/transformers group
uv run python -m unittest                # whole test suite (no API calls)
uv run python -m unittest tests.test_metrics                         # one module
uv run python -m unittest tests.test_metrics.OdsTests.test_always_pick_A_is_maximally_order_dependent  # one test
uv run ruff check .                      # lint; `--fix` for imports/spacing
uv run order-dependency preview --strategy cyclic --limit 1          # render prompts, no API calls
uv run order-dependency experiment --thinking disabled --effort low -o opus5-no-thinking   # -> <repo>/results/opus5-no-thinking
uv run order-dependency experiment -q mmlu --per-subject 20 -o mmlu-subset  # MMLU, fetched from Hugging Face and cached
uv run order-dependency experiment -q data/finance_extraction.json --thinking disabled -o finance-extraction   # extraction task
uv run order-dependency experiment -q data/apple_fy2025_mcq.json --thinking disabled -o apple-fy2025   # whole real 8-K as context, lettered options
```

`215_Large_Language_Models_Are_.pdf` at the repo root is Zheng et al. (ICLR 2024), the paper the
assignment references. `--strategy place-correct` reproduces its Table 1 "answer-moving attack";
the report's recall-by-position row is that table's A/B/C/D columns. PriDe (its debiasing algorithm)
is not implemented.

`experiment` needs `ANTHROPIC_API_KEY` with credit; it sends one probe request first and exits 1 with the
API error if that fails. Default `--strategy place-correct` asks each question once per option position
(4 prompts for a 4-option question); `--strategy full` asks all 24 orderings.

## Architecture

Pipeline: `MCQ` → permutations → `harnesses/` → `Trial` records → `analysis/` (`metrics.aggregate` → `report`).
`-q mmlu` bypasses the JSON loader: `mmlu.load_mmlu` fetches the `cais/mmlu` parquet with `huggingface_hub`
(cached) and converts it to `MCQ`s with ids `mmlu-<subject>-<row>`; `--per-subject` draws a seeded subset.

The central idea that ties the modules together is the **canonical-vs-presented distinction**.
`MCQ.options` are in canonical (input-file) order. A `Permutation` is a tuple where `perm[j]` is the
canonical option shown at presented position `j` (letter `LABELS[j]`). `prompt.parse_reply` returns
a *presented* position; the answerers map it through `permutations.to_canonical` so every `Trial` stores
both `position` (letter) and `canonical` (which option). All metrics work on `canonical`; only the
position-bias tables use `position`.

An `MCQ` with a non-empty `values` tuple is an **extraction item** (`data/finance_extraction.json`):
its options are document segments each carrying one figure, the prompt shows them unlabelled under
`Excerpt:`, and `parse_reply` matches the model's figure numerically to a presented value instead of
reading a letter. An `MCQ` with a `context` is shown that document under `Document:` before the
question; `mcq.load_questions` fills it from a `context_file` key (path relative to the question
file) so one filing is shared by many records. `data/apple_fy2025_mcq.json` (MMLU-pattern records
over the saved `apple_fy2025_8k_ex99-1.txt`) and `data/apple_fy2025_extraction.json` (the same
questions as four-line excerpts) both use distractors that share the answer's row label (other
period, other statement, GAAP vs non-GAAP). Reports use `MCQ.display` (values when present, else
options) as the short label.

`analysis/metrics.py`'s module docstring defines **ODS** (`Σ_o Var_p[P_p(o)] / (1 − 1/K)`) and the
supporting metrics; the tests in `tests/test_metrics.py` pin its endpoints (invariant answerer → 0,
always-"A" answerer → 1). Probabilities `P_p(o)` come from repeated samples, not log-probs — the API
does not expose them.

`runner/run_experiment.py` returns an `ExperimentRun` (pydantic model: config, permutation settings,
questions, trials). `analysis.report.write_report` computes metrics from it and writes `results.json`
(`model_dump()` + summary) / `trials.csv` / `report.md`. Because the record is self-contained,
`ExperimentRun.model_validate_json` can rebuild a saved run from `results.json`. `MCQ`, `Trial`, `LLMConfig` stay stdlib dataclasses; pydantic validates them as fields.

The `harnesses/` package holds two backends with the same `answer(mcq, perm_index, perm, sample) -> Trial`
method: `ClaudeAnswerer` (API, sampled letter) and `HFAnswerer` (local transformers model, argmax of
the option-letter logits after `Answer:`, fills `Trial.probabilities`). The `LLMConfig.answerer`
property builds the one selected by `backend`. Both modules import `LLMConfig` only under
`TYPE_CHECKING` because `llm_config` imports them; `hf_answerer` imports torch/transformers inside
the class because they live in the optional `hf` dependency group (`uv sync --group hf`).
The headline `ods` is always one-hot (chosen option per trial) so it compares across backends; when
`probabilities` are present `analysis.metrics` also reports `ods_probability` / `mean_ods_probability`
from the full letter distribution.

`runner/llm_config.py`'s `LLMConfig.request_kwargs()` is the single place the Anthropic request shape is built (`thinking`,
`output_config.effort`, no temperature — current Claude models reject sampling params). On refusal
or `max_tokens` the trial is recorded as unanswered; there is deliberately no fallback to another
model so a run measures exactly one model.

## Project Rules & Style Guidance

### Code Style & Constraints
- **Write minimal code:** Prioritize brevity, readability, and performance. Eliminate boilerplate, redundant logic, and over-engineering.
- **No placeholder text:** Write full, working implementations instead of leaving `// TODO` or `// Implement later` comments.
- **Keep files focused:** Prefer small, single-purpose helper functions over massive, monolithic blocks of code.
- **Dependencies:** Use built-in language features whenever possible. Do not install external libraries for trivial tasks.
- **No conversational fluff:** When generating code, output the code directly with minimal conversational explanation.

## Conventions (enforced by ruff config in pyproject.toml)

- One class per module, named after the class (`trial.py` → `Trial`).
- Absolute imports only (`from order_dependency.mcq import MCQ`); import blocks sorted and grouped.
- Google-style docstrings on every module/class/function (`D` rules, `convention = "google"`).
- Tests use stdlib `unittest`, not pytest, and cover intended behaviour on valid input only — no
  tests for invalid input, error paths or malformed model output.
- Line length 120.
- One expression per line: don't nest several calls or operations in a single expression. Bind
  intermediate results to named variables so each line does one thing — e.g. build the
  permutation list on one line and `sample` from it on the next, rather than
  `Random(seed).sample(list(permutations(identity)), min(n or k, len(...)))`. Chained tuple
  assignments (`a, b = x, y`) are fine.

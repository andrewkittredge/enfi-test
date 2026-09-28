# Order Dependency in LLM Answers to Multiple-Choice Questions

LLMs exhibit order dependency bias when answering multiple choice questions (MCQs), see Zheng et al. https://openreview.net/pdf?id=shr9PXz7T0.  Order dependency is when LLMs bias their answer based on the order of tokens in the prompt, i.e. the response to a prompt can change based merely on the order of the input without any change in semantics.  In the context of answering multiple choice questions, order dependency manifests as an LLM's bias towards selecting a choice based on position, for instance tending to select the first answer.

The `order-dependency` package passes MCQs to an LLM, records the responses and generates an analysis of the bias.

The project was substantially developed by `Claude Code` using the `Fable 5.1` model prompted to replicate Zheng.

## Example
Run a small example with local inference using the Qwen2.5-0.5B model-

```
uv run --group hf order-dependency experiment --backend hf --model Qwen/Qwen2.5-0.5B -q mmlu --per-subject 20 -o mmlu-qwen05b-subset
```

The output is written to `results/*`.  An example of an output report is included in this repository.


Commands to generate the rest of the data reported are below. The Claude runs need `ANTHROPIC_API_KEY`.

```
uv run order-dependency experiment --model claude-opus-5 --thinking disabled --effort low -q mmlu --per-subject 20 -o mmlu-opus5-no-thinking
uv run order-dependency experiment --model claude-haiku-4-5 --thinking omit --effort none -q mmlu --per-subject 20 -o mmlu-haiku45
uv run --group hf order-dependency experiment --backend hf --model huggyllama/llama-7b --quantize 4bit -q mmlu --per-subject 20 -o mmlu-llama7b-4bit
```

## Implementation

1. Build a list of questions/answers as an experimant, either the mmlu dataset downloaded from hugging face or a custom set passed by a path, see the example `order-dependency/data`.
2. For each question permutes the answers according to the passed strategy.
3. Build a prompt with the question/answers and passes it to the model.
4. Parse the responses from the model.
5. Pass the responses to the `analysis.metrics` module.
6. `analysis.metrics` computes the ODS score for each question and aggregates the results for the experiment.
7. `analysis.report` writes the analysis to the `/results` directory.

## Evaluation Methodology

The MMLU test set (Hendrycks et al.), 20 questions from each of its 57 subjects, 1,140 in
total, each asked under the four `place-correct` orderings: 4,560 prompts per model. Four models:
Claude Opus 5 (thinking disabled), Claude Haiku 4.5, and Qwen2.5-0.5B, a small open-weight base model
run locally as a stand-in for the models studied in the paper, and LLaMA-7B (`huggyllama/llama-7b`, one
of the models in the paper), run locally with 4-bit (bitsandbytes NF4) weights because the fp16 model
does not fit an 8 GB GPU (`results/mmlu-llama7b-4bit/`).

**Metrics.** ODS, consistency and majority vote are computed on which *option* the model chose, not
which letter; RStd and the letter shares are, by design, about position.

- **ODS** (Option Dependency Score): how much the model's choice of option moves when only the
  ordering changes, on a `[0, 1]` scale. Defined below.
  `P_p(o)` is the probability that the model picked option `o` when shown ordering `p`. ODS sums the variance of `P_p(o)` across orderings over the `K` options, scaled so the worst case is 1:

  ```
  ODS = sum_o Var_p[ P_p(o) ] / (1 - 1/K)
  ```
  A model that picks the same option under every ordering scores 0. A model that always answers "A"
picks a different option under each ordering and scores 1.
- **Questions with any change**, **consistency** (agreement with the question's modal answer) and
  **majority-vote accuracy** (accuracy of the modal option, a mitigation that comes free from the
  same data).
- **Answer-moving attack** (the paper's Table 1, reproduced in each run's `report.md`): accuracy with
  the gold option forced to each letter versus accuracy on the options as authored. Its standard
  deviation is **RStd**, and the share of answers landing on each letter shows position bias directly.

## Results

**Headline metrics** from each run's `report.md`.

| Metric | Claude Opus 5 | Claude Haiku 4.5 | Qwen2.5-0.5B | LLaMA-7B |
|---|---|---|---|---|
| Mean ODS (0 = order-invariant, 1 = fully order-determined) | 0.029 | 0.140 | 0.357 | 0.696 |
| Questions with at least one order-induced answer change | 57 / 1140 | 273 / 1140 | 668 / 1140 | 1113 / 1140 |
| Mean consistency (agreement with modal answer) | 98.3% | 91.8% | 79.1% | 58.9% |
| Accuracy per prompt (averaged over orderings) | 93.7% | 83.4% | 44.4% | 29.7% |


The results are robust and replicate Zheng et al. All four models saw the same 1,140 questions, so
the sampling error on each answer-change rate is under two points, far smaller than the gaps between
models. A second LLaMA-7B run, fp16 on 57 questions, gave the same picture as the 4-bit run: 96%
of questions changed answer, 30% accuracy, and the same preference for A and C. Zheng et al. report
33.7% accuracy and an RStd of 18.5 for llama-7B on 0-shot MMLU; the two runs here give 30% and
RStd 18.1 and 25.5. Their gpt-3.5-turbo had an RStd of 5.5, above Haiku 4.5 at 2.8 and Opus 5 at 0.3.

The data indicates order dependency is fading with newer models. LLaMA-7B (2023) changes its answer on 98% of questions and puts 93% of its picks on positions A or C: it chooses a position, not an option. Qwen2.5-0.5B (2024) changes on 59%, Claude Haiku 4.5 (2025) on 24%, Claude Opus 5 (2026) on 5%. 

## Financial Filing

*This example is a demonstration only and is not fully baked: the question set is small (18
hand-written questions over one filing), only two models were run, and the results have not been
checked to the standard of the MMLU runs above.*

MMLU questions are short and likely seen in training. `order-dependency/data/apple_fy2025_mcq.json` asks 18 questions
about Apple's fiscal 2025 fourth-quarter results with the full 8-K press release (about 4,300 tokens)
supplied as context in every prompt. The four options are figures from the same line of the filing
(the answer plus another period, another statement, or the GAAP rather than non-GAAP column), so they
cannot be separated without reading the document.

```
uv run order-dependency experiment --model claude-haiku-4-5 --thinking omit --effort none -q data/apple_fy2025_mcq.json --strategy full -o apple-fy2025-haiku
uv run --group hf order-dependency experiment --backend hf --model Qwen/Qwen2.5-0.5B -q data/apple_fy2025_mcq.json --strategy full -o apple-fy2025-qwen05b
```

**Headline metrics** from each run's `report.md`; `results/apple-fy2025-qwen05b/report.md` is the Qwen run's report.

| Metric | Claude Haiku 4.5 | Qwen2.5-0.5B |
|---|---|---|
| Mean ODS (0 = order-invariant, 1 = fully order-determined) | 0.000 | 0.906 |
| Questions with at least one order-induced answer change | 0 / 18 | 18 / 18 |
| Mean consistency (agreement with modal answer) | 100.0% | 38.7% |
| Accuracy per prompt (averaged over orderings) | 100.0% | 27.3% |



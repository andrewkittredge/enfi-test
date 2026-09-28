# Order dependency report

- Run at: 2026-09-30T20:11:06+00:00
- Model: `Qwen/Qwen2.5-0.5B` · local Hugging Face model, fp16, scored from option-letter logits
- Permutation strategy: `full` · samples per ordering: 1
- Prompts: 432 (0 unanswered/unparseable) · tokens in/out: 2,059,032/0

## Headline metrics

| Metric | Value |
|---|---|
| Mean ODS (0 = order-invariant, 1 = fully order-determined) | **0.906** |
| Median / max ODS | 0.958 / 1.000 |
| Mean ODS from option-letter probabilities | 0.066 |
| Questions with at least one order-induced answer change | 18 / 18 |
| Mean consistency (agreement with modal answer) | 38.7% |
| Accuracy per prompt (averaged over orderings) | 27.3% |
| Accuracy of permutation majority vote (mitigation) | 27.8% |
| Recall std across correct-answer positions (RStd) | 0.114 |

## Answer-moving attack (paper Table 1)

Accuracy on the options as authored (Orig), and accuracy when every question's correct option is moved to a fixed position; parentheses give the change in points versus Orig.

| Orig | Move gold to A | Move gold to B | Move gold to C | Move gold to D |
|---|---|---|---|---|
| 33.3% | 39.8% (+6.5) | 33.3% (+0.0) | 26.9% (-6.5) | 9.3% (-24.1) |

## Position bias

Share of answers landing on each displayed position, and accuracy when the correct option was displayed at that position (for extraction items, position A is the first line of the excerpt). A balanced permutation set should give a uniform share (~25.0%) and flat recall if the model ignores ordering.

| Position | A | B | C | D |
|---|---|---|---|---|
| Chosen share | 39.6% | 35.4% | 17.4% | 7.6% |
| Recall when correct is here | 39.8% | 33.3% | 26.9% | 9.3% |

## Per-question results

| ID | Topic | Difficulty | ODS | Consistency | Accuracy | Majority answer | Majority correct |
|---|---|---|---|---|---|---|---|
| aapl-products-cost-of-sales-q4 | statement of operations | medium | 1.000 | 25.0% | 25.0% | $73,716 million | no |
| aapl-cash-ending-fy25 | statement of cash flows | medium | 1.000 | 25.0% | 25.0% | $29,943 million | no |
| aapl-buybacks-fy25 | statement of cash flows | medium | 1.000 | 25.0% | 25.0% | $90,711 million | yes |
| aapl-term-debt-current | balance sheet | hard | 1.000 | 25.0% | 25.0% | $10,912 million | no |
| aapl-iphone-fy25 | net sales by category | medium | 0.995 | 29.2% | 25.0% | $49,025 million | no |
| aapl-tax-provision-gaap-q4-fy24 | non-GAAP reconciliation | hard | 0.995 | 29.2% | 25.0% | $5,338 million | no |
| aapl-services-net-sales-q4 | statement of operations | medium | 0.986 | 29.2% | 16.7% | $24,972 million | no |
| aapl-other-income-q4 | statement of operations | hard | 0.986 | 33.3% | 20.8% | $(321) million | no |
| aapl-marketable-securities-noncurrent | balance sheet | hard | 0.958 | 37.5% | 25.0% | $35,228 million | no |
| aapl-greater-china-q4 | net sales by segment | medium | 0.940 | 37.5% | 37.5% | $14,493 million | yes |
| aapl-net-income-non-gaap-fy24 | non-GAAP reconciliation | hard | 0.921 | 41.7% | 41.7% | $103,982 million | yes |
| aapl-shares-outstanding | balance sheet vs statement of operations | hard | 0.884 | 41.7% | 8.3% | 14,815,307 thousand | no |
| aapl-rd-fy25 | statement of operations | easy | 0.875 | 41.7% | 4.2% | $27,601 million | no |
| aapl-diluted-eps-fy25 | statement of operations | medium | 0.875 | 50.0% | 20.8% | $1.85 | no |
| aapl-accounts-receivable | balance sheet vs cash flows | hard | 0.875 | 45.8% | 12.5% | $(3,788) million | no |
| aapl-inventories | balance sheet vs cash flows | hard | 0.843 | 45.8% | 45.8% | $5,718 million | yes |
| aapl-dividend-per-share | press release | easy | 0.625 | 62.5% | 37.5% | $1.85 | no |
| aapl-state-aid-charge | non-GAAP reconciliation footnote | hard | 0.551 | 70.8% | 70.8% | $10.2 billion | yes |

## Discrepancies: same question, different orderings, different answers

### aapl-products-cost-of-sales-q4 - What was Apple's cost of sales for Products for the three months ended September 27, 2025?

Correct: **$47,019 million**. Options: $73,716 million; $47,019 million; $54,125 million; $194,116 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$73,716 million, B=$47,019 million, C=$54,125 million, D=$194,116 million | B | $73,716 million | no |
| A=$73,716 million, B=$47,019 million, C=$194,116 million, D=$54,125 million | B | $73,716 million | no |
| A=$73,716 million, B=$54,125 million, C=$47,019 million, D=$194,116 million | C | $73,716 million | no |
| A=$73,716 million, B=$54,125 million, C=$194,116 million, D=$47,019 million | D | $73,716 million | no |
| A=$73,716 million, B=$194,116 million, C=$47,019 million, D=$54,125 million | C | $73,716 million | no |
| A=$73,716 million, B=$194,116 million, C=$54,125 million, D=$47,019 million | D | $73,716 million | no |
| A=$47,019 million, B=$73,716 million, C=$54,125 million, D=$194,116 million | A | $47,019 million | yes |
| A=$47,019 million, B=$73,716 million, C=$194,116 million, D=$54,125 million | A | $47,019 million | yes |
| A=$47,019 million, B=$54,125 million, C=$73,716 million, D=$194,116 million | A | $47,019 million | yes |
| A=$47,019 million, B=$54,125 million, C=$194,116 million, D=$73,716 million | A | $47,019 million | yes |
| A=$47,019 million, B=$194,116 million, C=$73,716 million, D=$54,125 million | A | $47,019 million | yes |
| A=$47,019 million, B=$194,116 million, C=$54,125 million, D=$73,716 million | A | $47,019 million | yes |
| A=$54,125 million, B=$73,716 million, C=$47,019 million, D=$194,116 million | C | $54,125 million | no |
| A=$54,125 million, B=$73,716 million, C=$194,116 million, D=$47,019 million | D | $54,125 million | no |
| A=$54,125 million, B=$47,019 million, C=$73,716 million, D=$194,116 million | B | $54,125 million | no |
| A=$54,125 million, B=$47,019 million, C=$194,116 million, D=$73,716 million | B | $54,125 million | no |
| A=$54,125 million, B=$194,116 million, C=$73,716 million, D=$47,019 million | D | $54,125 million | no |
| A=$54,125 million, B=$194,116 million, C=$47,019 million, D=$73,716 million | C | $54,125 million | no |
| A=$194,116 million, B=$73,716 million, C=$47,019 million, D=$54,125 million | C | $194,116 million | no |
| A=$194,116 million, B=$73,716 million, C=$54,125 million, D=$47,019 million | D | $194,116 million | no |
| A=$194,116 million, B=$47,019 million, C=$73,716 million, D=$54,125 million | B | $194,116 million | no |
| A=$194,116 million, B=$47,019 million, C=$54,125 million, D=$73,716 million | B | $194,116 million | no |
| A=$194,116 million, B=$54,125 million, C=$73,716 million, D=$47,019 million | D | $194,116 million | no |
| A=$194,116 million, B=$54,125 million, C=$47,019 million, D=$73,716 million | C | $194,116 million | no |

### aapl-cash-ending-fy25 - What was Apple's ending balance of cash, cash equivalents, and restricted cash and cash equivalents for the twelve months ended September 27, 2025?

Correct: **$35,934 million**. Options: $29,943 million; $35,934 million; $5,991 million; $30,737 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$29,943 million, B=$35,934 million, C=$5,991 million, D=$30,737 million | B | $29,943 million | no |
| A=$29,943 million, B=$35,934 million, C=$30,737 million, D=$5,991 million | B | $29,943 million | no |
| A=$29,943 million, B=$5,991 million, C=$35,934 million, D=$30,737 million | C | $29,943 million | no |
| A=$29,943 million, B=$5,991 million, C=$30,737 million, D=$35,934 million | D | $29,943 million | no |
| A=$29,943 million, B=$30,737 million, C=$35,934 million, D=$5,991 million | C | $29,943 million | no |
| A=$29,943 million, B=$30,737 million, C=$5,991 million, D=$35,934 million | D | $29,943 million | no |
| A=$35,934 million, B=$29,943 million, C=$5,991 million, D=$30,737 million | A | $35,934 million | yes |
| A=$35,934 million, B=$29,943 million, C=$30,737 million, D=$5,991 million | A | $35,934 million | yes |
| A=$35,934 million, B=$5,991 million, C=$29,943 million, D=$30,737 million | A | $35,934 million | yes |
| A=$35,934 million, B=$5,991 million, C=$30,737 million, D=$29,943 million | A | $35,934 million | yes |
| A=$35,934 million, B=$30,737 million, C=$29,943 million, D=$5,991 million | A | $35,934 million | yes |
| A=$35,934 million, B=$30,737 million, C=$5,991 million, D=$29,943 million | A | $35,934 million | yes |
| A=$5,991 million, B=$29,943 million, C=$35,934 million, D=$30,737 million | C | $5,991 million | no |
| A=$5,991 million, B=$29,943 million, C=$30,737 million, D=$35,934 million | D | $5,991 million | no |
| A=$5,991 million, B=$35,934 million, C=$29,943 million, D=$30,737 million | B | $5,991 million | no |
| A=$5,991 million, B=$35,934 million, C=$30,737 million, D=$29,943 million | B | $5,991 million | no |
| A=$5,991 million, B=$30,737 million, C=$29,943 million, D=$35,934 million | D | $5,991 million | no |
| A=$5,991 million, B=$30,737 million, C=$35,934 million, D=$29,943 million | C | $5,991 million | no |
| A=$30,737 million, B=$29,943 million, C=$35,934 million, D=$5,991 million | C | $30,737 million | no |
| A=$30,737 million, B=$29,943 million, C=$5,991 million, D=$35,934 million | D | $30,737 million | no |
| A=$30,737 million, B=$35,934 million, C=$29,943 million, D=$5,991 million | B | $30,737 million | no |
| A=$30,737 million, B=$35,934 million, C=$5,991 million, D=$29,943 million | B | $30,737 million | no |
| A=$30,737 million, B=$5,991 million, C=$29,943 million, D=$35,934 million | D | $30,737 million | no |
| A=$30,737 million, B=$5,991 million, C=$35,934 million, D=$29,943 million | C | $30,737 million | no |

### aapl-buybacks-fy25 - How much cash did Apple use for repurchases of common stock in the twelve months ended September 27, 2025?

Correct: **$90,711 million**. Options: $90,711 million; $94,949 million; $15,421 million; $120,686 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$90,711 million, B=$94,949 million, C=$15,421 million, D=$120,686 million | A | $90,711 million | yes |
| A=$90,711 million, B=$94,949 million, C=$120,686 million, D=$15,421 million | A | $90,711 million | yes |
| A=$90,711 million, B=$15,421 million, C=$94,949 million, D=$120,686 million | A | $90,711 million | yes |
| A=$90,711 million, B=$15,421 million, C=$120,686 million, D=$94,949 million | A | $90,711 million | yes |
| A=$90,711 million, B=$120,686 million, C=$94,949 million, D=$15,421 million | A | $90,711 million | yes |
| A=$90,711 million, B=$120,686 million, C=$15,421 million, D=$94,949 million | A | $90,711 million | yes |
| A=$94,949 million, B=$90,711 million, C=$15,421 million, D=$120,686 million | B | $94,949 million | no |
| A=$94,949 million, B=$90,711 million, C=$120,686 million, D=$15,421 million | B | $94,949 million | no |
| A=$94,949 million, B=$15,421 million, C=$90,711 million, D=$120,686 million | C | $94,949 million | no |
| A=$94,949 million, B=$15,421 million, C=$120,686 million, D=$90,711 million | D | $94,949 million | no |
| A=$94,949 million, B=$120,686 million, C=$90,711 million, D=$15,421 million | C | $94,949 million | no |
| A=$94,949 million, B=$120,686 million, C=$15,421 million, D=$90,711 million | D | $94,949 million | no |
| A=$15,421 million, B=$90,711 million, C=$94,949 million, D=$120,686 million | B | $15,421 million | no |
| A=$15,421 million, B=$90,711 million, C=$120,686 million, D=$94,949 million | B | $15,421 million | no |
| A=$15,421 million, B=$94,949 million, C=$90,711 million, D=$120,686 million | C | $15,421 million | no |
| A=$15,421 million, B=$94,949 million, C=$120,686 million, D=$90,711 million | D | $15,421 million | no |
| A=$15,421 million, B=$120,686 million, C=$90,711 million, D=$94,949 million | C | $15,421 million | no |
| A=$15,421 million, B=$120,686 million, C=$94,949 million, D=$90,711 million | D | $15,421 million | no |
| A=$120,686 million, B=$90,711 million, C=$94,949 million, D=$15,421 million | B | $120,686 million | no |
| A=$120,686 million, B=$90,711 million, C=$15,421 million, D=$94,949 million | B | $120,686 million | no |
| A=$120,686 million, B=$94,949 million, C=$90,711 million, D=$15,421 million | C | $120,686 million | no |
| A=$120,686 million, B=$94,949 million, C=$15,421 million, D=$90,711 million | D | $120,686 million | no |
| A=$120,686 million, B=$15,421 million, C=$90,711 million, D=$94,949 million | C | $120,686 million | no |
| A=$120,686 million, B=$15,421 million, C=$94,949 million, D=$90,711 million | D | $120,686 million | no |

### aapl-term-debt-current - How much of Apple's term debt was classified as a current liability as of September 27, 2025?

Correct: **$12,350 million**. Options: $12,350 million; $10,912 million; $78,328 million; $85,750 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$12,350 million, B=$10,912 million, C=$78,328 million, D=$85,750 million | A | $10,912 million | no |
| A=$12,350 million, B=$10,912 million, C=$85,750 million, D=$78,328 million | A | $10,912 million | no |
| A=$12,350 million, B=$78,328 million, C=$10,912 million, D=$85,750 million | A | $78,328 million | no |
| A=$12,350 million, B=$78,328 million, C=$85,750 million, D=$10,912 million | A | $78,328 million | no |
| A=$12,350 million, B=$85,750 million, C=$10,912 million, D=$78,328 million | A | $85,750 million | no |
| A=$12,350 million, B=$85,750 million, C=$78,328 million, D=$10,912 million | A | $85,750 million | no |
| A=$10,912 million, B=$12,350 million, C=$78,328 million, D=$85,750 million | B | $12,350 million | yes |
| A=$10,912 million, B=$12,350 million, C=$85,750 million, D=$78,328 million | B | $12,350 million | yes |
| A=$10,912 million, B=$78,328 million, C=$12,350 million, D=$85,750 million | C | $78,328 million | no |
| A=$10,912 million, B=$78,328 million, C=$85,750 million, D=$12,350 million | D | $78,328 million | no |
| A=$10,912 million, B=$85,750 million, C=$12,350 million, D=$78,328 million | C | $85,750 million | no |
| A=$10,912 million, B=$85,750 million, C=$78,328 million, D=$12,350 million | D | $85,750 million | no |
| A=$78,328 million, B=$12,350 million, C=$10,912 million, D=$85,750 million | B | $12,350 million | yes |
| A=$78,328 million, B=$12,350 million, C=$85,750 million, D=$10,912 million | B | $12,350 million | yes |
| A=$78,328 million, B=$10,912 million, C=$12,350 million, D=$85,750 million | C | $10,912 million | no |
| A=$78,328 million, B=$10,912 million, C=$85,750 million, D=$12,350 million | D | $10,912 million | no |
| A=$78,328 million, B=$85,750 million, C=$12,350 million, D=$10,912 million | C | $85,750 million | no |
| A=$78,328 million, B=$85,750 million, C=$10,912 million, D=$12,350 million | D | $85,750 million | no |
| A=$85,750 million, B=$12,350 million, C=$10,912 million, D=$78,328 million | B | $12,350 million | yes |
| A=$85,750 million, B=$12,350 million, C=$78,328 million, D=$10,912 million | B | $12,350 million | yes |
| A=$85,750 million, B=$10,912 million, C=$12,350 million, D=$78,328 million | C | $10,912 million | no |
| A=$85,750 million, B=$10,912 million, C=$78,328 million, D=$12,350 million | D | $10,912 million | no |
| A=$85,750 million, B=$78,328 million, C=$12,350 million, D=$10,912 million | C | $78,328 million | no |
| A=$85,750 million, B=$78,328 million, C=$10,912 million, D=$12,350 million | D | $78,328 million | no |

### aapl-iphone-fy25 - What were Apple's iPhone net sales for the twelve months ended September 27, 2025?

Correct: **$209,586 million**. Options: $209,586 million; $201,183 million; $49,025 million; $46,222 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$209,586 million, B=$201,183 million, C=$49,025 million, D=$46,222 million | A | $209,586 million | yes |
| A=$209,586 million, B=$201,183 million, C=$46,222 million, D=$49,025 million | A | $209,586 million | yes |
| A=$209,586 million, B=$49,025 million, C=$201,183 million, D=$46,222 million | A | $209,586 million | yes |
| A=$209,586 million, B=$49,025 million, C=$46,222 million, D=$201,183 million | A | $209,586 million | yes |
| A=$209,586 million, B=$46,222 million, C=$201,183 million, D=$49,025 million | A | $209,586 million | yes |
| A=$209,586 million, B=$46,222 million, C=$49,025 million, D=$201,183 million | A | $209,586 million | yes |
| A=$201,183 million, B=$209,586 million, C=$49,025 million, D=$46,222 million | B | $201,183 million | no |
| A=$201,183 million, B=$209,586 million, C=$46,222 million, D=$49,025 million | B | $201,183 million | no |
| A=$201,183 million, B=$49,025 million, C=$209,586 million, D=$46,222 million | C | $201,183 million | no |
| A=$201,183 million, B=$49,025 million, C=$46,222 million, D=$209,586 million | D | $201,183 million | no |
| A=$201,183 million, B=$46,222 million, C=$209,586 million, D=$49,025 million | C | $201,183 million | no |
| A=$201,183 million, B=$46,222 million, C=$49,025 million, D=$209,586 million | D | $201,183 million | no |
| A=$49,025 million, B=$209,586 million, C=$201,183 million, D=$46,222 million | B | $49,025 million | no |
| A=$49,025 million, B=$209,586 million, C=$46,222 million, D=$201,183 million | B | $49,025 million | no |
| A=$49,025 million, B=$201,183 million, C=$209,586 million, D=$46,222 million | C | $49,025 million | no |
| A=$49,025 million, B=$201,183 million, C=$46,222 million, D=$209,586 million | D | $49,025 million | no |
| A=$49,025 million, B=$46,222 million, C=$209,586 million, D=$201,183 million | C | $49,025 million | no |
| A=$49,025 million, B=$46,222 million, C=$201,183 million, D=$209,586 million | D | $49,025 million | no |
| A=$46,222 million, B=$209,586 million, C=$201,183 million, D=$49,025 million | B | $46,222 million | no |
| A=$46,222 million, B=$209,586 million, C=$49,025 million, D=$201,183 million | B | $46,222 million | no |
| A=$46,222 million, B=$201,183 million, C=$209,586 million, D=$49,025 million | C | $46,222 million | no |
| A=$46,222 million, B=$201,183 million, C=$49,025 million, D=$209,586 million | D | $46,222 million | no |
| A=$46,222 million, B=$49,025 million, C=$209,586 million, D=$201,183 million | C | $46,222 million | no |
| A=$46,222 million, B=$49,025 million, C=$201,183 million, D=$209,586 million | D | $49,025 million | no |

### aapl-tax-provision-gaap-q4-fy24 - As reported under GAAP, what was Apple's provision for income taxes for the three months ended September 28, 2024?

Correct: **$14,874 million**. Options: $14,874 million; $4,628 million; $5,338 million; $29,749 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$14,874 million, B=$4,628 million, C=$5,338 million, D=$29,749 million | A | $14,874 million | yes |
| A=$14,874 million, B=$4,628 million, C=$29,749 million, D=$5,338 million | A | $14,874 million | yes |
| A=$14,874 million, B=$5,338 million, C=$4,628 million, D=$29,749 million | A | $14,874 million | yes |
| A=$14,874 million, B=$5,338 million, C=$29,749 million, D=$4,628 million | A | $14,874 million | yes |
| A=$14,874 million, B=$29,749 million, C=$4,628 million, D=$5,338 million | A | $14,874 million | yes |
| A=$14,874 million, B=$29,749 million, C=$5,338 million, D=$4,628 million | A | $14,874 million | yes |
| A=$4,628 million, B=$14,874 million, C=$5,338 million, D=$29,749 million | B | $4,628 million | no |
| A=$4,628 million, B=$14,874 million, C=$29,749 million, D=$5,338 million | B | $4,628 million | no |
| A=$4,628 million, B=$5,338 million, C=$14,874 million, D=$29,749 million | C | $4,628 million | no |
| A=$4,628 million, B=$5,338 million, C=$29,749 million, D=$14,874 million | D | $5,338 million | no |
| A=$4,628 million, B=$29,749 million, C=$14,874 million, D=$5,338 million | C | $4,628 million | no |
| A=$4,628 million, B=$29,749 million, C=$5,338 million, D=$14,874 million | D | $4,628 million | no |
| A=$5,338 million, B=$14,874 million, C=$4,628 million, D=$29,749 million | B | $5,338 million | no |
| A=$5,338 million, B=$14,874 million, C=$29,749 million, D=$4,628 million | B | $5,338 million | no |
| A=$5,338 million, B=$4,628 million, C=$14,874 million, D=$29,749 million | C | $5,338 million | no |
| A=$5,338 million, B=$4,628 million, C=$29,749 million, D=$14,874 million | D | $5,338 million | no |
| A=$5,338 million, B=$29,749 million, C=$14,874 million, D=$4,628 million | C | $5,338 million | no |
| A=$5,338 million, B=$29,749 million, C=$4,628 million, D=$14,874 million | D | $5,338 million | no |
| A=$29,749 million, B=$14,874 million, C=$4,628 million, D=$5,338 million | B | $29,749 million | no |
| A=$29,749 million, B=$14,874 million, C=$5,338 million, D=$4,628 million | B | $29,749 million | no |
| A=$29,749 million, B=$4,628 million, C=$14,874 million, D=$5,338 million | C | $29,749 million | no |
| A=$29,749 million, B=$4,628 million, C=$5,338 million, D=$14,874 million | D | $29,749 million | no |
| A=$29,749 million, B=$5,338 million, C=$14,874 million, D=$4,628 million | C | $29,749 million | no |
| A=$29,749 million, B=$5,338 million, C=$4,628 million, D=$14,874 million | D | $29,749 million | no |

### aapl-services-net-sales-q4 - What were Apple's Services net sales for the three months ended September 27, 2025?

Correct: **$28,750 million**. Options: $28,750 million; $24,972 million; $7,106 million; $109,158 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$28,750 million, B=$24,972 million, C=$7,106 million, D=$109,158 million | A | $24,972 million | no |
| A=$28,750 million, B=$24,972 million, C=$109,158 million, D=$7,106 million | A | $24,972 million | no |
| A=$28,750 million, B=$7,106 million, C=$24,972 million, D=$109,158 million | A | $7,106 million | no |
| A=$28,750 million, B=$7,106 million, C=$109,158 million, D=$24,972 million | A | $7,106 million | no |
| A=$28,750 million, B=$109,158 million, C=$24,972 million, D=$7,106 million | A | $109,158 million | no |
| A=$28,750 million, B=$109,158 million, C=$7,106 million, D=$24,972 million | A | $109,158 million | no |
| A=$24,972 million, B=$28,750 million, C=$7,106 million, D=$109,158 million | B | $28,750 million | yes |
| A=$24,972 million, B=$28,750 million, C=$109,158 million, D=$7,106 million | B | $28,750 million | yes |
| A=$24,972 million, B=$7,106 million, C=$28,750 million, D=$109,158 million | C | $7,106 million | no |
| A=$24,972 million, B=$7,106 million, C=$109,158 million, D=$28,750 million | D | $7,106 million | no |
| A=$24,972 million, B=$109,158 million, C=$28,750 million, D=$7,106 million | C | $109,158 million | no |
| A=$24,972 million, B=$109,158 million, C=$7,106 million, D=$28,750 million | D | $109,158 million | no |
| A=$7,106 million, B=$28,750 million, C=$24,972 million, D=$109,158 million | B | $28,750 million | yes |
| A=$7,106 million, B=$28,750 million, C=$109,158 million, D=$24,972 million | B | $28,750 million | yes |
| A=$7,106 million, B=$24,972 million, C=$28,750 million, D=$109,158 million | C | $24,972 million | no |
| A=$7,106 million, B=$24,972 million, C=$109,158 million, D=$28,750 million | D | $24,972 million | no |
| A=$7,106 million, B=$109,158 million, C=$28,750 million, D=$24,972 million | C | $109,158 million | no |
| A=$7,106 million, B=$109,158 million, C=$24,972 million, D=$28,750 million | D | $109,158 million | no |
| A=$109,158 million, B=$28,750 million, C=$24,972 million, D=$7,106 million | B | $24,972 million | no |
| A=$109,158 million, B=$28,750 million, C=$7,106 million, D=$24,972 million | B | $7,106 million | no |
| A=$109,158 million, B=$24,972 million, C=$28,750 million, D=$7,106 million | C | $24,972 million | no |
| A=$109,158 million, B=$24,972 million, C=$7,106 million, D=$28,750 million | D | $24,972 million | no |
| A=$109,158 million, B=$7,106 million, C=$28,750 million, D=$24,972 million | C | $7,106 million | no |
| A=$109,158 million, B=$7,106 million, C=$24,972 million, D=$28,750 million | D | $7,106 million | no |

### aapl-other-income-q4 - What was Apple's other income/(expense), net for the three months ended September 27, 2025?

Correct: **$377 million**. Options: $377 million; $19 million; $(321) million; $269 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$377 million, B=$19 million, C=$(321) million, D=$269 million | A | $(321) million | no |
| A=$377 million, B=$19 million, C=$269 million, D=$(321) million | A | $269 million | no |
| A=$377 million, B=$(321) million, C=$19 million, D=$269 million | A | $269 million | no |
| A=$377 million, B=$(321) million, C=$269 million, D=$19 million | A | $269 million | no |
| A=$377 million, B=$269 million, C=$19 million, D=$(321) million | A | $(321) million | no |
| A=$377 million, B=$269 million, C=$(321) million, D=$19 million | A | $19 million | no |
| A=$19 million, B=$377 million, C=$(321) million, D=$269 million | B | $(321) million | no |
| A=$19 million, B=$377 million, C=$269 million, D=$(321) million | B | $(321) million | no |
| A=$19 million, B=$(321) million, C=$377 million, D=$269 million | C | $377 million | yes |
| A=$19 million, B=$(321) million, C=$269 million, D=$377 million | D | $269 million | no |
| A=$19 million, B=$269 million, C=$377 million, D=$(321) million | C | $(321) million | no |
| A=$19 million, B=$269 million, C=$(321) million, D=$377 million | D | $377 million | yes |
| A=$(321) million, B=$377 million, C=$19 million, D=$269 million | B | $269 million | no |
| A=$(321) million, B=$377 million, C=$269 million, D=$19 million | B | $19 million | no |
| A=$(321) million, B=$19 million, C=$377 million, D=$269 million | C | $269 million | no |
| A=$(321) million, B=$19 million, C=$269 million, D=$377 million | D | $377 million | yes |
| A=$(321) million, B=$269 million, C=$377 million, D=$19 million | C | $19 million | no |
| A=$(321) million, B=$269 million, C=$19 million, D=$377 million | D | $377 million | yes |
| A=$269 million, B=$377 million, C=$19 million, D=$(321) million | B | $(321) million | no |
| A=$269 million, B=$377 million, C=$(321) million, D=$19 million | B | $19 million | no |
| A=$269 million, B=$19 million, C=$377 million, D=$(321) million | C | $(321) million | no |
| A=$269 million, B=$19 million, C=$(321) million, D=$377 million | D | $(321) million | no |
| A=$269 million, B=$(321) million, C=$377 million, D=$19 million | C | $19 million | no |
| A=$269 million, B=$(321) million, C=$19 million, D=$377 million | D | $377 million | yes |

### aapl-marketable-securities-noncurrent - What was the carrying amount of Apple's non-current marketable securities as of September 27, 2025?

Correct: **$77,723 million**. Options: $18,763 million; $35,228 million; $77,723 million; $91,479 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$18,763 million, B=$35,228 million, C=$77,723 million, D=$91,479 million | C | $35,228 million | no |
| A=$18,763 million, B=$35,228 million, C=$91,479 million, D=$77,723 million | D | $35,228 million | no |
| A=$18,763 million, B=$77,723 million, C=$35,228 million, D=$91,479 million | B | $77,723 million | yes |
| A=$18,763 million, B=$77,723 million, C=$91,479 million, D=$35,228 million | B | $77,723 million | yes |
| A=$18,763 million, B=$91,479 million, C=$35,228 million, D=$77,723 million | D | $91,479 million | no |
| A=$18,763 million, B=$91,479 million, C=$77,723 million, D=$35,228 million | C | $91,479 million | no |
| A=$35,228 million, B=$18,763 million, C=$77,723 million, D=$91,479 million | C | $35,228 million | no |
| A=$35,228 million, B=$18,763 million, C=$91,479 million, D=$77,723 million | D | $18,763 million | no |
| A=$35,228 million, B=$77,723 million, C=$18,763 million, D=$91,479 million | B | $35,228 million | no |
| A=$35,228 million, B=$77,723 million, C=$91,479 million, D=$18,763 million | B | $35,228 million | no |
| A=$35,228 million, B=$91,479 million, C=$18,763 million, D=$77,723 million | D | $91,479 million | no |
| A=$35,228 million, B=$91,479 million, C=$77,723 million, D=$18,763 million | C | $91,479 million | no |
| A=$77,723 million, B=$18,763 million, C=$35,228 million, D=$91,479 million | A | $77,723 million | yes |
| A=$77,723 million, B=$18,763 million, C=$91,479 million, D=$35,228 million | A | $77,723 million | yes |
| A=$77,723 million, B=$35,228 million, C=$18,763 million, D=$91,479 million | A | $35,228 million | no |
| A=$77,723 million, B=$35,228 million, C=$91,479 million, D=$18,763 million | A | $35,228 million | no |
| A=$77,723 million, B=$91,479 million, C=$18,763 million, D=$35,228 million | A | $91,479 million | no |
| A=$77,723 million, B=$91,479 million, C=$35,228 million, D=$18,763 million | A | $91,479 million | no |
| A=$91,479 million, B=$18,763 million, C=$35,228 million, D=$77,723 million | D | $18,763 million | no |
| A=$91,479 million, B=$18,763 million, C=$77,723 million, D=$35,228 million | C | $18,763 million | no |
| A=$91,479 million, B=$35,228 million, C=$18,763 million, D=$77,723 million | D | $35,228 million | no |
| A=$91,479 million, B=$35,228 million, C=$77,723 million, D=$18,763 million | C | $35,228 million | no |
| A=$91,479 million, B=$77,723 million, C=$18,763 million, D=$35,228 million | B | $77,723 million | yes |
| A=$91,479 million, B=$77,723 million, C=$35,228 million, D=$18,763 million | B | $77,723 million | yes |

### aapl-greater-china-q4 - What were Apple's Greater China net sales for the three months ended September 27, 2025?

Correct: **$14,493 million**. Options: $14,493 million; $15,033 million; $64,377 million; $66,952 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$14,493 million, B=$15,033 million, C=$64,377 million, D=$66,952 million | A | $15,033 million | no |
| A=$14,493 million, B=$15,033 million, C=$66,952 million, D=$64,377 million | A | $15,033 million | no |
| A=$14,493 million, B=$64,377 million, C=$15,033 million, D=$66,952 million | A | $15,033 million | no |
| A=$14,493 million, B=$64,377 million, C=$66,952 million, D=$15,033 million | A | $66,952 million | no |
| A=$14,493 million, B=$66,952 million, C=$15,033 million, D=$64,377 million | A | $15,033 million | no |
| A=$14,493 million, B=$66,952 million, C=$64,377 million, D=$15,033 million | A | $66,952 million | no |
| A=$15,033 million, B=$14,493 million, C=$64,377 million, D=$66,952 million | B | $14,493 million | yes |
| A=$15,033 million, B=$14,493 million, C=$66,952 million, D=$64,377 million | B | $14,493 million | yes |
| A=$15,033 million, B=$64,377 million, C=$14,493 million, D=$66,952 million | C | $14,493 million | yes |
| A=$15,033 million, B=$64,377 million, C=$66,952 million, D=$14,493 million | D | $66,952 million | no |
| A=$15,033 million, B=$66,952 million, C=$14,493 million, D=$64,377 million | C | $14,493 million | yes |
| A=$15,033 million, B=$66,952 million, C=$64,377 million, D=$14,493 million | D | $66,952 million | no |
| A=$64,377 million, B=$14,493 million, C=$15,033 million, D=$66,952 million | B | $14,493 million | yes |
| A=$64,377 million, B=$14,493 million, C=$66,952 million, D=$15,033 million | B | $14,493 million | yes |
| A=$64,377 million, B=$15,033 million, C=$14,493 million, D=$66,952 million | C | $14,493 million | yes |
| A=$64,377 million, B=$15,033 million, C=$66,952 million, D=$14,493 million | D | $66,952 million | no |
| A=$64,377 million, B=$66,952 million, C=$14,493 million, D=$15,033 million | C | $66,952 million | no |
| A=$64,377 million, B=$66,952 million, C=$15,033 million, D=$14,493 million | D | $66,952 million | no |
| A=$66,952 million, B=$14,493 million, C=$15,033 million, D=$64,377 million | B | $15,033 million | no |
| A=$66,952 million, B=$14,493 million, C=$64,377 million, D=$15,033 million | B | $64,377 million | no |
| A=$66,952 million, B=$15,033 million, C=$14,493 million, D=$64,377 million | C | $14,493 million | yes |
| A=$66,952 million, B=$15,033 million, C=$64,377 million, D=$14,493 million | D | $64,377 million | no |
| A=$66,952 million, B=$64,377 million, C=$14,493 million, D=$15,033 million | C | $14,493 million | yes |
| A=$66,952 million, B=$64,377 million, C=$15,033 million, D=$14,493 million | D | $15,033 million | no |

### aapl-net-income-non-gaap-fy24 - What was Apple's net income as adjusted (non-GAAP) for the twelve months ended September 28, 2024?

Correct: **$103,982 million**. Options: $93,736 million; $10,246 million; $103,982 million; $112,010 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$93,736 million, B=$10,246 million, C=$103,982 million, D=$112,010 million | C | $103,982 million | yes |
| A=$93,736 million, B=$10,246 million, C=$112,010 million, D=$103,982 million | D | $103,982 million | yes |
| A=$93,736 million, B=$103,982 million, C=$10,246 million, D=$112,010 million | B | $10,246 million | no |
| A=$93,736 million, B=$103,982 million, C=$112,010 million, D=$10,246 million | B | $10,246 million | no |
| A=$93,736 million, B=$112,010 million, C=$10,246 million, D=$103,982 million | D | $10,246 million | no |
| A=$93,736 million, B=$112,010 million, C=$103,982 million, D=$10,246 million | C | $103,982 million | yes |
| A=$10,246 million, B=$93,736 million, C=$103,982 million, D=$112,010 million | C | $103,982 million | yes |
| A=$10,246 million, B=$93,736 million, C=$112,010 million, D=$103,982 million | D | $103,982 million | yes |
| A=$10,246 million, B=$103,982 million, C=$93,736 million, D=$112,010 million | B | $93,736 million | no |
| A=$10,246 million, B=$103,982 million, C=$112,010 million, D=$93,736 million | B | $93,736 million | no |
| A=$10,246 million, B=$112,010 million, C=$93,736 million, D=$103,982 million | D | $93,736 million | no |
| A=$10,246 million, B=$112,010 million, C=$103,982 million, D=$93,736 million | C | $103,982 million | yes |
| A=$103,982 million, B=$93,736 million, C=$10,246 million, D=$112,010 million | A | $112,010 million | no |
| A=$103,982 million, B=$93,736 million, C=$112,010 million, D=$10,246 million | A | $10,246 million | no |
| A=$103,982 million, B=$10,246 million, C=$93,736 million, D=$112,010 million | A | $112,010 million | no |
| A=$103,982 million, B=$10,246 million, C=$112,010 million, D=$93,736 million | A | $93,736 million | no |
| A=$103,982 million, B=$112,010 million, C=$93,736 million, D=$10,246 million | A | $10,246 million | no |
| A=$103,982 million, B=$112,010 million, C=$10,246 million, D=$93,736 million | A | $93,736 million | no |
| A=$112,010 million, B=$93,736 million, C=$10,246 million, D=$103,982 million | D | $103,982 million | yes |
| A=$112,010 million, B=$93,736 million, C=$103,982 million, D=$10,246 million | C | $103,982 million | yes |
| A=$112,010 million, B=$10,246 million, C=$93,736 million, D=$103,982 million | D | $103,982 million | yes |
| A=$112,010 million, B=$10,246 million, C=$103,982 million, D=$93,736 million | C | $103,982 million | yes |
| A=$112,010 million, B=$103,982 million, C=$93,736 million, D=$10,246 million | B | $10,246 million | no |
| A=$112,010 million, B=$103,982 million, C=$10,246 million, D=$93,736 million | B | $10,246 million | no |

### aapl-shares-outstanding - How many shares of Apple common stock were issued and outstanding as of September 27, 2025?

Correct: **14,773,260 thousand**. Options: 14,773,260 thousand; 15,116,786 thousand; 14,815,307 thousand; 14,863,609 thousand

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=14,773,260 thousand, B=15,116,786 thousand, C=14,815,307 thousand, D=14,863,609 thousand | A | 15,116,786 thousand | no |
| A=14,773,260 thousand, B=15,116,786 thousand, C=14,863,609 thousand, D=14,815,307 thousand | A | 15,116,786 thousand | no |
| A=14,773,260 thousand, B=14,815,307 thousand, C=15,116,786 thousand, D=14,863,609 thousand | A | 14,815,307 thousand | no |
| A=14,773,260 thousand, B=14,815,307 thousand, C=14,863,609 thousand, D=15,116,786 thousand | A | 14,815,307 thousand | no |
| A=14,773,260 thousand, B=14,863,609 thousand, C=15,116,786 thousand, D=14,815,307 thousand | A | 14,863,609 thousand | no |
| A=14,773,260 thousand, B=14,863,609 thousand, C=14,815,307 thousand, D=15,116,786 thousand | A | 14,863,609 thousand | no |
| A=15,116,786 thousand, B=14,773,260 thousand, C=14,815,307 thousand, D=14,863,609 thousand | B | 14,773,260 thousand | yes |
| A=15,116,786 thousand, B=14,773,260 thousand, C=14,863,609 thousand, D=14,815,307 thousand | B | 14,773,260 thousand | yes |
| A=15,116,786 thousand, B=14,815,307 thousand, C=14,773,260 thousand, D=14,863,609 thousand | C | 14,815,307 thousand | no |
| A=15,116,786 thousand, B=14,815,307 thousand, C=14,863,609 thousand, D=14,773,260 thousand | D | 14,815,307 thousand | no |
| A=15,116,786 thousand, B=14,863,609 thousand, C=14,773,260 thousand, D=14,815,307 thousand | C | 14,863,609 thousand | no |
| A=15,116,786 thousand, B=14,863,609 thousand, C=14,815,307 thousand, D=14,773,260 thousand | D | 14,863,609 thousand | no |
| A=14,815,307 thousand, B=14,773,260 thousand, C=15,116,786 thousand, D=14,863,609 thousand | B | 14,815,307 thousand | no |
| A=14,815,307 thousand, B=14,773,260 thousand, C=14,863,609 thousand, D=15,116,786 thousand | B | 14,815,307 thousand | no |
| A=14,815,307 thousand, B=15,116,786 thousand, C=14,773,260 thousand, D=14,863,609 thousand | C | 14,815,307 thousand | no |
| A=14,815,307 thousand, B=15,116,786 thousand, C=14,863,609 thousand, D=14,773,260 thousand | D | 14,815,307 thousand | no |
| A=14,815,307 thousand, B=14,863,609 thousand, C=14,773,260 thousand, D=15,116,786 thousand | C | 14,863,609 thousand | no |
| A=14,815,307 thousand, B=14,863,609 thousand, C=15,116,786 thousand, D=14,773,260 thousand | D | 14,863,609 thousand | no |
| A=14,863,609 thousand, B=14,773,260 thousand, C=15,116,786 thousand, D=14,815,307 thousand | B | 14,863,609 thousand | no |
| A=14,863,609 thousand, B=14,773,260 thousand, C=14,815,307 thousand, D=15,116,786 thousand | B | 14,863,609 thousand | no |
| A=14,863,609 thousand, B=15,116,786 thousand, C=14,773,260 thousand, D=14,815,307 thousand | C | 15,116,786 thousand | no |
| A=14,863,609 thousand, B=15,116,786 thousand, C=14,815,307 thousand, D=14,773,260 thousand | D | 14,863,609 thousand | no |
| A=14,863,609 thousand, B=14,815,307 thousand, C=14,773,260 thousand, D=15,116,786 thousand | C | 14,815,307 thousand | no |
| A=14,863,609 thousand, B=14,815,307 thousand, C=15,116,786 thousand, D=14,773,260 thousand | D | 14,815,307 thousand | no |

### aapl-rd-fy25 - What was Apple's research and development expense for the twelve months ended September 27, 2025?

Correct: **$34,550 million**. Options: $34,550 million; $31,370 million; $27,601 million; $62,151 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$34,550 million, B=$31,370 million, C=$27,601 million, D=$62,151 million | A | $31,370 million | no |
| A=$34,550 million, B=$31,370 million, C=$62,151 million, D=$27,601 million | A | $31,370 million | no |
| A=$34,550 million, B=$27,601 million, C=$31,370 million, D=$62,151 million | A | $27,601 million | no |
| A=$34,550 million, B=$27,601 million, C=$62,151 million, D=$31,370 million | A | $27,601 million | no |
| A=$34,550 million, B=$62,151 million, C=$31,370 million, D=$27,601 million | A | $34,550 million | yes |
| A=$34,550 million, B=$62,151 million, C=$27,601 million, D=$31,370 million | A | $62,151 million | no |
| A=$31,370 million, B=$34,550 million, C=$27,601 million, D=$62,151 million | B | $31,370 million | no |
| A=$31,370 million, B=$34,550 million, C=$62,151 million, D=$27,601 million | B | $31,370 million | no |
| A=$31,370 million, B=$27,601 million, C=$34,550 million, D=$62,151 million | C | $27,601 million | no |
| A=$31,370 million, B=$27,601 million, C=$62,151 million, D=$34,550 million | D | $31,370 million | no |
| A=$31,370 million, B=$62,151 million, C=$34,550 million, D=$27,601 million | C | $31,370 million | no |
| A=$31,370 million, B=$62,151 million, C=$27,601 million, D=$34,550 million | D | $62,151 million | no |
| A=$27,601 million, B=$34,550 million, C=$31,370 million, D=$62,151 million | B | $27,601 million | no |
| A=$27,601 million, B=$34,550 million, C=$62,151 million, D=$31,370 million | B | $27,601 million | no |
| A=$27,601 million, B=$31,370 million, C=$34,550 million, D=$62,151 million | C | $31,370 million | no |
| A=$27,601 million, B=$31,370 million, C=$62,151 million, D=$34,550 million | D | $27,601 million | no |
| A=$27,601 million, B=$62,151 million, C=$34,550 million, D=$31,370 million | C | $27,601 million | no |
| A=$27,601 million, B=$62,151 million, C=$31,370 million, D=$34,550 million | D | $27,601 million | no |
| A=$62,151 million, B=$34,550 million, C=$31,370 million, D=$27,601 million | B | $62,151 million | no |
| A=$62,151 million, B=$34,550 million, C=$27,601 million, D=$31,370 million | B | $62,151 million | no |
| A=$62,151 million, B=$31,370 million, C=$34,550 million, D=$27,601 million | C | $31,370 million | no |
| A=$62,151 million, B=$31,370 million, C=$27,601 million, D=$34,550 million | D | $31,370 million | no |
| A=$62,151 million, B=$27,601 million, C=$34,550 million, D=$31,370 million | C | $27,601 million | no |
| A=$62,151 million, B=$27,601 million, C=$31,370 million, D=$34,550 million | D | $27,601 million | no |

### aapl-diluted-eps-fy25 - What was Apple's diluted earnings per share for the twelve months ended September 27, 2025?

Correct: **$7.46**. Options: $7.46; $7.49; $6.08; $1.85

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$7.46, B=$7.49, C=$6.08, D=$1.85 | A | $6.08 | no |
| A=$7.46, B=$7.49, C=$1.85, D=$6.08 | A | $1.85 | no |
| A=$7.46, B=$6.08, C=$7.49, D=$1.85 | A | $7.49 | no |
| A=$7.46, B=$6.08, C=$1.85, D=$7.49 | A | $1.85 | no |
| A=$7.46, B=$1.85, C=$7.49, D=$6.08 | A | $1.85 | no |
| A=$7.46, B=$1.85, C=$6.08, D=$7.49 | A | $1.85 | no |
| A=$7.49, B=$7.46, C=$6.08, D=$1.85 | B | $6.08 | no |
| A=$7.49, B=$7.46, C=$1.85, D=$6.08 | B | $1.85 | no |
| A=$7.49, B=$6.08, C=$7.46, D=$1.85 | C | $7.46 | yes |
| A=$7.49, B=$6.08, C=$1.85, D=$7.46 | D | $1.85 | no |
| A=$7.49, B=$1.85, C=$7.46, D=$6.08 | C | $1.85 | no |
| A=$7.49, B=$1.85, C=$6.08, D=$7.46 | D | $1.85 | no |
| A=$6.08, B=$7.46, C=$7.49, D=$1.85 | B | $7.49 | no |
| A=$6.08, B=$7.46, C=$1.85, D=$7.49 | B | $1.85 | no |
| A=$6.08, B=$7.49, C=$7.46, D=$1.85 | C | $7.46 | yes |
| A=$6.08, B=$7.49, C=$1.85, D=$7.46 | D | $1.85 | no |
| A=$6.08, B=$1.85, C=$7.46, D=$7.49 | C | $1.85 | no |
| A=$6.08, B=$1.85, C=$7.49, D=$7.46 | D | $1.85 | no |
| A=$1.85, B=$7.46, C=$7.49, D=$6.08 | B | $6.08 | no |
| A=$1.85, B=$7.46, C=$6.08, D=$7.49 | B | $6.08 | no |
| A=$1.85, B=$7.49, C=$7.46, D=$6.08 | C | $7.46 | yes |
| A=$1.85, B=$7.49, C=$6.08, D=$7.46 | D | $6.08 | no |
| A=$1.85, B=$6.08, C=$7.46, D=$7.49 | C | $7.46 | yes |
| A=$1.85, B=$6.08, C=$7.49, D=$7.46 | D | $7.46 | yes |

### aapl-accounts-receivable - What was Apple's accounts receivable, net, as reported on the balance sheet as of September 27, 2025?

Correct: **$39,777 million**. Options: $39,777 million; $33,410 million; $(6,682) million; $(3,788) million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$39,777 million, B=$33,410 million, C=$(6,682) million, D=$(3,788) million | A | $39,777 million | yes |
| A=$39,777 million, B=$33,410 million, C=$(3,788) million, D=$(6,682) million | A | $39,777 million | yes |
| A=$39,777 million, B=$(6,682) million, C=$33,410 million, D=$(3,788) million | A | $(6,682) million | no |
| A=$39,777 million, B=$(6,682) million, C=$(3,788) million, D=$33,410 million | A | $(6,682) million | no |
| A=$39,777 million, B=$(3,788) million, C=$33,410 million, D=$(6,682) million | A | $39,777 million | yes |
| A=$39,777 million, B=$(3,788) million, C=$(6,682) million, D=$33,410 million | A | $(3,788) million | no |
| A=$33,410 million, B=$39,777 million, C=$(6,682) million, D=$(3,788) million | B | $33,410 million | no |
| A=$33,410 million, B=$39,777 million, C=$(3,788) million, D=$(6,682) million | B | $33,410 million | no |
| A=$33,410 million, B=$(6,682) million, C=$39,777 million, D=$(3,788) million | C | $(6,682) million | no |
| A=$33,410 million, B=$(6,682) million, C=$(3,788) million, D=$39,777 million | D | $(6,682) million | no |
| A=$33,410 million, B=$(3,788) million, C=$39,777 million, D=$(6,682) million | C | $(3,788) million | no |
| A=$33,410 million, B=$(3,788) million, C=$(6,682) million, D=$39,777 million | D | $(3,788) million | no |
| A=$(6,682) million, B=$39,777 million, C=$33,410 million, D=$(3,788) million | B | $(6,682) million | no |
| A=$(6,682) million, B=$39,777 million, C=$(3,788) million, D=$33,410 million | B | $(6,682) million | no |
| A=$(6,682) million, B=$33,410 million, C=$39,777 million, D=$(3,788) million | C | $(6,682) million | no |
| A=$(6,682) million, B=$33,410 million, C=$(3,788) million, D=$39,777 million | D | $(6,682) million | no |
| A=$(6,682) million, B=$(3,788) million, C=$39,777 million, D=$33,410 million | C | $(3,788) million | no |
| A=$(6,682) million, B=$(3,788) million, C=$33,410 million, D=$39,777 million | D | $(3,788) million | no |
| A=$(3,788) million, B=$39,777 million, C=$33,410 million, D=$(6,682) million | B | $(3,788) million | no |
| A=$(3,788) million, B=$39,777 million, C=$(6,682) million, D=$33,410 million | B | $(3,788) million | no |
| A=$(3,788) million, B=$33,410 million, C=$39,777 million, D=$(6,682) million | C | $(3,788) million | no |
| A=$(3,788) million, B=$33,410 million, C=$(6,682) million, D=$39,777 million | D | $(3,788) million | no |
| A=$(3,788) million, B=$(6,682) million, C=$39,777 million, D=$33,410 million | C | $(3,788) million | no |
| A=$(3,788) million, B=$(6,682) million, C=$33,410 million, D=$39,777 million | D | $(3,788) million | no |

### aapl-inventories - What were Apple's inventories as reported on the balance sheet as of September 27, 2025?

Correct: **$5,718 million**. Options: $5,718 million; $7,286 million; $1,400 million; $(1,046) million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$5,718 million, B=$7,286 million, C=$1,400 million, D=$(1,046) million | A | $7,286 million | no |
| A=$5,718 million, B=$7,286 million, C=$(1,046) million, D=$1,400 million | A | $(1,046) million | no |
| A=$5,718 million, B=$1,400 million, C=$7,286 million, D=$(1,046) million | A | $7,286 million | no |
| A=$5,718 million, B=$1,400 million, C=$(1,046) million, D=$7,286 million | A | $(1,046) million | no |
| A=$5,718 million, B=$(1,046) million, C=$7,286 million, D=$1,400 million | A | $(1,046) million | no |
| A=$5,718 million, B=$(1,046) million, C=$1,400 million, D=$7,286 million | A | $(1,046) million | no |
| A=$7,286 million, B=$5,718 million, C=$1,400 million, D=$(1,046) million | B | $5,718 million | yes |
| A=$7,286 million, B=$5,718 million, C=$(1,046) million, D=$1,400 million | B | $5,718 million | yes |
| A=$7,286 million, B=$1,400 million, C=$5,718 million, D=$(1,046) million | C | $5,718 million | yes |
| A=$7,286 million, B=$1,400 million, C=$(1,046) million, D=$5,718 million | D | $(1,046) million | no |
| A=$7,286 million, B=$(1,046) million, C=$5,718 million, D=$1,400 million | C | $5,718 million | yes |
| A=$7,286 million, B=$(1,046) million, C=$1,400 million, D=$5,718 million | D | $(1,046) million | no |
| A=$1,400 million, B=$5,718 million, C=$7,286 million, D=$(1,046) million | B | $5,718 million | yes |
| A=$1,400 million, B=$5,718 million, C=$(1,046) million, D=$7,286 million | B | $5,718 million | yes |
| A=$1,400 million, B=$7,286 million, C=$5,718 million, D=$(1,046) million | C | $5,718 million | yes |
| A=$1,400 million, B=$7,286 million, C=$(1,046) million, D=$5,718 million | D | $(1,046) million | no |
| A=$1,400 million, B=$(1,046) million, C=$5,718 million, D=$7,286 million | C | $(1,046) million | no |
| A=$1,400 million, B=$(1,046) million, C=$7,286 million, D=$5,718 million | D | $(1,046) million | no |
| A=$(1,046) million, B=$5,718 million, C=$7,286 million, D=$1,400 million | B | $5,718 million | yes |
| A=$(1,046) million, B=$5,718 million, C=$1,400 million, D=$7,286 million | B | $5,718 million | yes |
| A=$(1,046) million, B=$7,286 million, C=$5,718 million, D=$1,400 million | C | $5,718 million | yes |
| A=$(1,046) million, B=$7,286 million, C=$1,400 million, D=$5,718 million | D | $7,286 million | no |
| A=$(1,046) million, B=$1,400 million, C=$5,718 million, D=$7,286 million | C | $5,718 million | yes |
| A=$(1,046) million, B=$1,400 million, C=$7,286 million, D=$5,718 million | D | $1,400 million | no |

### aapl-dividend-per-share - What cash dividend per share did Apple's board of directors declare in this announcement?

Correct: **$0.26**. Options: $0.26; $1.85; $7.49; $15,421 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$0.26, B=$1.85, C=$7.49, D=$15,421 million | A | $1.85 | no |
| A=$0.26, B=$1.85, C=$15,421 million, D=$7.49 | A | $1.85 | no |
| A=$0.26, B=$7.49, C=$1.85, D=$15,421 million | A | $1.85 | no |
| A=$0.26, B=$7.49, C=$15,421 million, D=$1.85 | A | $0.26 | yes |
| A=$0.26, B=$15,421 million, C=$1.85, D=$7.49 | A | $1.85 | no |
| A=$0.26, B=$15,421 million, C=$7.49, D=$1.85 | A | $0.26 | yes |
| A=$1.85, B=$0.26, C=$7.49, D=$15,421 million | B | $1.85 | no |
| A=$1.85, B=$0.26, C=$15,421 million, D=$7.49 | B | $0.26 | yes |
| A=$1.85, B=$7.49, C=$0.26, D=$15,421 million | C | $1.85 | no |
| A=$1.85, B=$7.49, C=$15,421 million, D=$0.26 | D | $1.85 | no |
| A=$1.85, B=$15,421 million, C=$0.26, D=$7.49 | C | $1.85 | no |
| A=$1.85, B=$15,421 million, C=$7.49, D=$0.26 | D | $1.85 | no |
| A=$7.49, B=$0.26, C=$1.85, D=$15,421 million | B | $1.85 | no |
| A=$7.49, B=$0.26, C=$15,421 million, D=$1.85 | B | $0.26 | yes |
| A=$7.49, B=$1.85, C=$0.26, D=$15,421 million | C | $1.85 | no |
| A=$7.49, B=$1.85, C=$15,421 million, D=$0.26 | D | $1.85 | no |
| A=$7.49, B=$15,421 million, C=$0.26, D=$1.85 | C | $0.26 | yes |
| A=$7.49, B=$15,421 million, C=$1.85, D=$0.26 | D | $1.85 | no |
| A=$15,421 million, B=$0.26, C=$1.85, D=$7.49 | B | $0.26 | yes |
| A=$15,421 million, B=$0.26, C=$7.49, D=$1.85 | B | $0.26 | yes |
| A=$15,421 million, B=$1.85, C=$0.26, D=$7.49 | C | $1.85 | no |
| A=$15,421 million, B=$1.85, C=$7.49, D=$0.26 | D | $1.85 | no |
| A=$15,421 million, B=$7.49, C=$0.26, D=$1.85 | C | $0.26 | yes |
| A=$15,421 million, B=$7.49, C=$1.85, D=$0.26 | D | $0.26 | yes |

### aapl-state-aid-charge - What was the net amount of the one-time income tax charge Apple recorded in the fourth quarter of 2024 relating to the European Commission's State Aid decision?

Correct: **$10.2 billion**. Options: $10.2 billion; $15.8 billion; $4.8 billion; $823 million

| Ordering (A, B, ...) | Correct at | Answer | Correct? |
|---|---|---|---|
| A=$10.2 billion, B=$15.8 billion, C=$4.8 billion, D=$823 million | A | $10.2 billion | yes |
| A=$10.2 billion, B=$15.8 billion, C=$823 million, D=$4.8 billion | A | $10.2 billion | yes |
| A=$10.2 billion, B=$4.8 billion, C=$15.8 billion, D=$823 million | A | $10.2 billion | yes |
| A=$10.2 billion, B=$4.8 billion, C=$823 million, D=$15.8 billion | A | $10.2 billion | yes |
| A=$10.2 billion, B=$823 million, C=$15.8 billion, D=$4.8 billion | A | $15.8 billion | no |
| A=$10.2 billion, B=$823 million, C=$4.8 billion, D=$15.8 billion | A | $10.2 billion | yes |
| A=$15.8 billion, B=$10.2 billion, C=$4.8 billion, D=$823 million | B | $10.2 billion | yes |
| A=$15.8 billion, B=$10.2 billion, C=$823 million, D=$4.8 billion | B | $10.2 billion | yes |
| A=$15.8 billion, B=$4.8 billion, C=$10.2 billion, D=$823 million | C | $10.2 billion | yes |
| A=$15.8 billion, B=$4.8 billion, C=$823 million, D=$10.2 billion | D | $15.8 billion | no |
| A=$15.8 billion, B=$823 million, C=$10.2 billion, D=$4.8 billion | C | $10.2 billion | yes |
| A=$15.8 billion, B=$823 million, C=$4.8 billion, D=$10.2 billion | D | $15.8 billion | no |
| A=$4.8 billion, B=$10.2 billion, C=$15.8 billion, D=$823 million | B | $10.2 billion | yes |
| A=$4.8 billion, B=$10.2 billion, C=$823 million, D=$15.8 billion | B | $10.2 billion | yes |
| A=$4.8 billion, B=$15.8 billion, C=$10.2 billion, D=$823 million | C | $10.2 billion | yes |
| A=$4.8 billion, B=$15.8 billion, C=$823 million, D=$10.2 billion | D | $15.8 billion | no |
| A=$4.8 billion, B=$823 million, C=$10.2 billion, D=$15.8 billion | C | $10.2 billion | yes |
| A=$4.8 billion, B=$823 million, C=$15.8 billion, D=$10.2 billion | D | $15.8 billion | no |
| A=$823 million, B=$10.2 billion, C=$15.8 billion, D=$4.8 billion | B | $10.2 billion | yes |
| A=$823 million, B=$10.2 billion, C=$4.8 billion, D=$15.8 billion | B | $10.2 billion | yes |
| A=$823 million, B=$15.8 billion, C=$10.2 billion, D=$4.8 billion | C | $10.2 billion | yes |
| A=$823 million, B=$15.8 billion, C=$4.8 billion, D=$10.2 billion | D | $15.8 billion | no |
| A=$823 million, B=$4.8 billion, C=$10.2 billion, D=$15.8 billion | C | $10.2 billion | yes |
| A=$823 million, B=$4.8 billion, C=$15.8 billion, D=$10.2 billion | D | $15.8 billion | no |

## Questions used

- **aapl-rd-fy25** (statement of operations, easy): What was Apple's research and development expense for the twelve months ended September 27, 2025?
  - $34,550 million  ✅
  - $31,370 million
  - $27,601 million
  - $62,151 million
- **aapl-dividend-per-share** (press release, easy): What cash dividend per share did Apple's board of directors declare in this announcement?
  - $0.26  ✅
  - $1.85
  - $7.49
  - $15,421 million
- **aapl-services-net-sales-q4** (statement of operations, medium): What were Apple's Services net sales for the three months ended September 27, 2025?
  - $28,750 million  ✅
  - $24,972 million
  - $7,106 million
  - $109,158 million
- **aapl-iphone-fy25** (net sales by category, medium): What were Apple's iPhone net sales for the twelve months ended September 27, 2025?
  - $209,586 million  ✅
  - $201,183 million
  - $49,025 million
  - $46,222 million
- **aapl-greater-china-q4** (net sales by segment, medium): What were Apple's Greater China net sales for the three months ended September 27, 2025?
  - $14,493 million  ✅
  - $15,033 million
  - $64,377 million
  - $66,952 million
- **aapl-products-cost-of-sales-q4** (statement of operations, medium): What was Apple's cost of sales for Products for the three months ended September 27, 2025?
  - $73,716 million
  - $47,019 million  ✅
  - $54,125 million
  - $194,116 million
- **aapl-diluted-eps-fy25** (statement of operations, medium): What was Apple's diluted earnings per share for the twelve months ended September 27, 2025?
  - $7.46  ✅
  - $7.49
  - $6.08
  - $1.85
- **aapl-cash-ending-fy25** (statement of cash flows, medium): What was Apple's ending balance of cash, cash equivalents, and restricted cash and cash equivalents for the twelve months ended September 27, 2025?
  - $29,943 million
  - $35,934 million  ✅
  - $5,991 million
  - $30,737 million
- **aapl-buybacks-fy25** (statement of cash flows, medium): How much cash did Apple use for repurchases of common stock in the twelve months ended September 27, 2025?
  - $90,711 million  ✅
  - $94,949 million
  - $15,421 million
  - $120,686 million
- **aapl-other-income-q4** (statement of operations, hard): What was Apple's other income/(expense), net for the three months ended September 27, 2025?
  - $377 million  ✅
  - $19 million
  - $(321) million
  - $269 million
- **aapl-marketable-securities-noncurrent** (balance sheet, hard): What was the carrying amount of Apple's non-current marketable securities as of September 27, 2025?
  - $18,763 million
  - $35,228 million
  - $77,723 million  ✅
  - $91,479 million
- **aapl-term-debt-current** (balance sheet, hard): How much of Apple's term debt was classified as a current liability as of September 27, 2025?
  - $12,350 million  ✅
  - $10,912 million
  - $78,328 million
  - $85,750 million
- **aapl-accounts-receivable** (balance sheet vs cash flows, hard): What was Apple's accounts receivable, net, as reported on the balance sheet as of September 27, 2025?
  - $39,777 million  ✅
  - $33,410 million
  - $(6,682) million
  - $(3,788) million
- **aapl-inventories** (balance sheet vs cash flows, hard): What were Apple's inventories as reported on the balance sheet as of September 27, 2025?
  - $5,718 million  ✅
  - $7,286 million
  - $1,400 million
  - $(1,046) million
- **aapl-shares-outstanding** (balance sheet vs statement of operations, hard): How many shares of Apple common stock were issued and outstanding as of September 27, 2025?
  - 14,773,260 thousand  ✅
  - 15,116,786 thousand
  - 14,815,307 thousand
  - 14,863,609 thousand
- **aapl-tax-provision-gaap-q4-fy24** (non-GAAP reconciliation, hard): As reported under GAAP, what was Apple's provision for income taxes for the three months ended September 28, 2024?
  - $14,874 million  ✅
  - $4,628 million
  - $5,338 million
  - $29,749 million
- **aapl-net-income-non-gaap-fy24** (non-GAAP reconciliation, hard): What was Apple's net income as adjusted (non-GAAP) for the twelve months ended September 28, 2024?
  - $93,736 million
  - $10,246 million
  - $103,982 million  ✅
  - $112,010 million
- **aapl-state-aid-charge** (non-GAAP reconciliation footnote, hard): What was the net amount of the one-time income tax charge Apple recorded in the fourth quarter of 2024 relating to the European Commission's State Aid decision?
  - $10.2 billion  ✅
  - $15.8 billion
  - $4.8 billion
  - $823 million

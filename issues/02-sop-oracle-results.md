---
title: "[decision] Selection-Matched Text RAG (SOP-Oracle) results are not in the code repository"
labels: decision, data-integrity, priority-high
---
**Question:** Where is the run behind RQ2?

**Evidence:** The paper reports Selection-Matched Text RAG at 0.962 KFR, 0.975 coverage, 1,479 prompt tokens, and a paired difference of -0.007 [-0.036, 0.021], p = 0.59. No oracle system, generation log, or score exists on any branch of `code/` (checked `exp/full-run-v1`, `main`, `fix/*`, `feature/*`).

**Options**
1. Commit the oracle implementation and its results (summary, per-query scores, significance) to `code/`, then cite the run id in the paper.
2. If the run does not exist, run it with the same seed and settings; until then the RQ2 numbers cannot be reported.

**Note:** `\showoraclefalse` in the preamble hides the oracle values in the figures.

---
title: "[task] Refusal scorer misses the fixed template \"tidak menemukan\" (code repo)"
labels: task, experiment, cross-repo
---
Section 6.3: the benchmark refusal patterns omit the substring "tidak menemukan", so the deterministic Naive RAG template is scored as a non-refusal (8 answerable queries get KFR 0 without counting as false refusals; NA-4 and NA-5 count as failed refusals). Fix the pattern in `code/benchmark/sop_benchmark_v1.json`, re-score (no regeneration needed), and decide whether the paper reports the corrected or the original numbers.

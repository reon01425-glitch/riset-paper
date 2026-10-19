---
name: paper-densify
description: Iteratively tighten a LaTeX research paper to a page and word budget with parallel subagents - one reviewer, one figure/table designer, one number auditor, and one densifier per section - looping until the measurable targets pass. Use when the user asks to make a paper denser, shorter, less wandering, or to add data-grounded figures and tables.
disable-model-invocation: true
---

# Paper densify loop

You are the orchestrator. You do not rewrite sections yourself; you measure, plan,
dispatch subagents in parallel, merge their output, and measure again. Every claim
and number in the paper must stay traceable to the repository data.

Arguments (from `$ARGUMENTS`, or ask once if missing):
- `TEX`: the paper's main .tex file.
- `DATA`: the repository folder holding the results (e.g. `results/full_v3_20261008/`,
  `results/full_base_20261008/`, `benchmark/`, `src/graph_sop/`, `data/*.pdf`).
- `LAYOUT`: the layout the page limit refers to: `twocol` (Elsevier final, two columns)
  or `asis` (preprint, single column). Default `twocol`.
- Targets (defaults, change only if the user says so):
  - pages without references in `LAYOUT`: **8 to 13**, aim for 11 to 12;
  - words, measured in `asis`: **6,000 to 7,500 including references** (the journal checker counts the
    reference list), aim near 7,200 including references (about 6,500 without);
  - 0 Type 3 fonts, 0 Overfull boxes, 0 undefined references, every float cited.

Read `style_rules.md` (same folder) before planning. It defines "dense" and "wandering".

## Iteration loop (at most 3 iterations unless the user asks for more)

### 0. Set up
1. Copy `TEX` to a new version file (e.g. `paper_v8_6.tex`); never edit the previous version.
2. Baseline: `python3 .claude/skills/paper-densify/scripts/measure.py <new>.tex` and
   `... --layout <LAYOUT>`. Keep the old PDF as the baseline for number checks.
3. Split: `python3 .claude/skills/paper-densify/scripts/sections.py split <new>.tex work/iterN`.
   `00_preamble.tex` and `99_back.tex` are not edited by agents.

### 1. Diagnose, in parallel (one message, three Agent calls)
- `fresh-reviewer`: give it only the compiled PDF path and `style_rules.md`, not this
  conversation. It returns a per-paragraph verdict (keep / tighten / merge / cut / move-to-figure).
- `figure-table-designer`: give it `DATA`, the section files, and the current float list.
  It returns at most 3 candidate floats, each with its data source, the prose it replaces,
  its estimated word and page cost, and ready-to-compile LaTeX in `work/iterN/floats/`.
- `number-auditor`: give it `TEX` and `DATA`. It returns every number in the paper that
  is not traceable to a data file, plus known open issues.

### 2. Plan (you, briefly)
Write `work/iterN/plan.md`: for each section file, a word budget, the reviewer verdicts to
apply, and which floats it must reference. Accept a candidate float only if it answers a
research question or replaces at least ~80 words of prose, and the page budget still fits.
Budgets must add up to the targets; spend words on Results and Method, not on Related work.

### 3. Densify, in parallel (one Agent call per section file, all in one message)
Each `section-densifier` gets: its own section file path, its budget and verdicts from
`plan.md`, `style_rules.md`, the float labels it must cite, and the glossary in
`style_rules.md`. It overwrites only its own file. It must not add numbers that are not
already in the paper or in `DATA`, and must keep every \label, \cite, and float.

### 4. Merge and verify
1. `python3 .claude/skills/paper-densify/scripts/sections.py merge work/iterN <new>.tex`
2. Insert accepted floats where `plan.md` says.
3. Measure in both layouts with `--baseline <previous>.pdf`.
   Any number in "numbers lost vs baseline" must be either intentionally removed
   (note why in `plan.md`) or restored.
4. Run `number-auditor` again on the merged file. Fix every new untraceable number.
5. Look at every page that has a new or changed float (render with `pdftoppm` and view it).

### 5. Stop or repeat
Stop when all targets pass and the reviewer's second pass marks no paragraph as
`cut` or `wander`. Otherwise start the next iteration from step 1 on the merged file.

## Report to the user
One short table: pages (both layouts), words, floats, and what changed per section;
the list of intentionally removed numbers; and any open issue the auditor raised that
needs the author's decision. Do not resolve author decisions (for example, which audit
numbers are real) on your own.

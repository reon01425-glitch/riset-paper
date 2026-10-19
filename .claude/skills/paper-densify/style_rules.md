# Style rules: dense, not wandering

## A dense paragraph
1. Opens with a topic sentence that states one claim (a finding, a design decision, or a definition).
2. Gives the evidence for that claim: the one to three numbers that carry it, or a pointer to the
   table/figure that holds the rest ("Table 7"), never both the pointer and a recital of the table.
3. Ends with the consequence for a research question (RQ1 to RQ4) or a contribution, in one sentence.
4. 80 to 160 words. Sentences of 30 words or fewer. No sentence that only announces what comes next.

## Signs of wandering (cut or merge these)
- Meta sentences: "In this section we...", "It is important to note that...", "As mentioned above...".
- A caveat repeated outside Section 7 (threats). State each caveat once, in one place, then refer to it.
- Restating numbers that a table or figure already shows, beyond the ones the claim needs.
- Background the reader does not need to follow the method (history of RAG, generic LLM claims).
- The same result reported in Results, Discussion, and Conclusion with the same numbers.
  Results: the numbers. Discussion: what they mean. Conclusion: one sentence per RQ, no new numbers.
- Enumerations of more than four items in prose: make them a table or a figure.
- A paragraph whose removal would not weaken any RQ answer or contribution.

## What must never change
- Any number, unless the number auditor shows it is wrong or the plan removes it on purpose.
- Every \label, \ref, \cite, equation, and float environment.
- The honesty statements: non-significance is not equivalence; the entity-graph baseline is
  custom; the benchmark was author-verified; the audit scope; single generator.
  Keep each once (Section 7), not zero times.
- Claims cannot become stronger than the data. "Prevents" or "guarantees" needs a test that shows it.

## Glossary (use exactly one name per concept)
Workflow GraphRAG (proposed) | Selection-Matched Text RAG (the ablation; logged as SOP-Oracle RAG) |
Naive RAG | GraphRAG (entity) or "the entity-graph baseline" | full-context prompting | LLM only |
key-fact recall (KFR) | step coverage | Topological Inversion Rate (TIR) | Actor Mismatch Rate (AMR) |
SOP | procedure (same thing, use SOP in tables) | actor (role that performs a step).

## Figures and tables (house style)
- TikZ/pgfplots in the .tex, no external images. `\scriptsize` text inside floats.
- Proposed components: `blue!70!black` border, `blue!6` fill. Neutral boxes: black on white.
  Panels: `gray!6` fill, `gray!50` border, rounded corners 3pt.
- Every figure must be readable in grayscale: pair colour with marker shape or line style.
- Captions: two sentences at most. Say what is shown and the one thing to notice.
- Width `\textwidth` with `\resizebox`; in two-column layout the measure script turns floats into `figure*`.

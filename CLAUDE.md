# Project memory for the SOP-RAG paper

- Paper: `paper/paper_v9_0_cas_dc.tex` (Elsevier CAS double-column template `cas-dc`, target journal: Natural Language Processing Journal, Elsevier).
  Compile with pdflatex three times; tables come from `paper/paper_tables/*.tex`; supplementary tables S1-S3 in `paper/supplementary.tex`.
  Content source for the CAS and Word versions: `paper/paper_v9_0_elsarticle.tex` (regenerate with `tools/cas/make_cas.sh` and `tools/docx/make_docx.sh`).
- Versioning: one git tag per paper version (v8.2 ... v9.0); built PDFs/DOCX live in `builds/<version>/`. Work items are GitHub issues (see `issues/`).
- Data: the `code/` submodule (Chatbot-RAG-Comparison, branch `exp/full-run-v1`, pinned commit 4163ed8). Main run `results/full_v3_20261008/`, base-embedding run `results/full_base_20261008/`,
  benchmark `benchmark/sop_benchmark_v1.json`, workflow graph `src/graph_sop/workflow_graph.py` (7 root, 44 step, 15 actor nodes, 125 edges), SOP PDFs in `data/`.
- Supervisor constraint: written simply; about 15 pages including references, i.e. 8-13 pages without references. Journal checker: 6,000-7,500 words, and it counts the reference list too (v8.5 at 7,270 without references was still flagged). v9.0 (cas-dc): 7,139 words including references, 12 pages, references start on p12. Running headers add about 200 words to a raw PDF text count.
- Open author decisions (do not resolve silently; report them):
  1. The paper reports a 60-row audit (0.983 / kappa 0.955); `audit_agreement.json` says only 14/60 rows were reviewed (0.857).
  2. Selection-Matched Text RAG (SOP-Oracle) results (0.962 KFR, 1,479 tokens, p = 0.59) are not in the repository on any branch.
- Fonts: keep `\input{glyphtounicode}` and `\pdfgentounicode=1` so checkers can read ligatures. cas-dc uses STIX/Charis when installed (MacTeX has both).

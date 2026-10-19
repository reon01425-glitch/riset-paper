---
title: "[task] Add ORCID iDs for all seven authors"
labels: task, submission
---
The CAS class always prints an `ORCID(s):` footnote, so v9.0 hides it with `\RenewDocumentCommand{\printorcid}{}{}`.

**Done when:** each `\author[..]{..}` has `[orcid=0000-...]` in `paper/paper_v9_0_cas_dc.tex` (and the generator `tools/cas/convert.py`), and the override line is deleted.

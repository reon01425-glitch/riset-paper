---
title: "[task] Single source for LaTeX (CAS) and Word versions"
labels: task, infrastructure
---
`paper/paper_v9_0_elsarticle.tex` is the content source; `tools/cas/make_cas.sh` and `tools/docx/make_docx.sh` generate the CAS and Word versions. The Claude Code kit edits `paper_v9_0_cas_dc.tex` directly, so edits can diverge. Pick one canonical file and make both generators read it.

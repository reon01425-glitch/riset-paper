# Procedure Selection versus Workflow Structuring in Local RAG for Institutional SOP Question Answering

Manuscript repository for the ablation paper by C.F. Wiratama, I. Waspada, D.K. Fu'adi, R. Ramli, H. Tantyoko,
S. Kurniawan, and S.R. Purnama (Universitas Diponegoro; Universiti Sains Malaysia).
Target journal: *Natural Language Processing Journal* (Elsevier).

The experiment code, benchmark, and results live in the [Chatbot-RAG-Comparison](https://github.com/reon01425-glitch/Chatbot-RAG-Comparison)
repository, included here as the `code/` submodule pinned to the commit the paper reports (`exp/full-run-v1`, 4163ed8).

## Current version: v9.0

| File | What |
|---|---|
| `builds/v9.0/paper_v9_0_cas_dc.pdf` | Elsevier CAS double-column layout (12 pages; 11 without references) |
| `builds/v9.0/paper_v9_0_cas_sc.pdf` | CAS single-column layout (16 pages) |
| `builds/v9.0/paper_v9_0.docx` | Word version (figures as 300-dpi images) |
| `builds/v9.0/paper_v9_0_supplementary.pdf` | Supplementary Tables S1 to S3 |
| `paper/highlights.txt` | Highlights, submitted as a separate file |

Word count of v9.0: 7,139 words including references (6,402 excluding references); journal limit 6,000 to 7,500.

## Layout

```
paper/            LaTeX sources of the current version
  paper_v9_0_elsarticle.tex   content source (edit this, then regenerate)
  paper_v9_0_cas_dc.tex       generated CAS double-column version
  paper_v9_0_cas_sc.tex       generated CAS single-column version
  paper_tables/               tables and \newcommand numbers
  parts/                      figure and table snippets added in v8.3 and v8.5
builds/<version>/ compiled PDFs and DOCX for every version
figures/          standalone figures
tools/cas/        elsarticle -> CAS converter (make_cas.sh)
tools/docx/       LaTeX -> Word pipeline (make_docx.sh)
.claude/, CLAUDE.md  Claude Code skill and subagents for iterative tightening (docs/claude-code.md)
issues/           issue drafts; issues/create_issues.sh files them on GitHub
code/             submodule: experiment code and results
```

## Versions

Every version is a git tag; `git checkout v8.5` restores that version's sources, and `builds/` keeps every compiled file.
See [CHANGELOG.md](CHANGELOG.md).

## Build

Requires TeX Live or MacTeX (pdflatex, lmodern, stix), and for Word also pandoc 3 and Python 3.

```bash
git clone --recurse-submodules https://github.com/reon01425-glitch/riset-paper
tools/cas/make_cas.sh                                # CAS PDFs from paper/paper_v9_0_elsarticle.tex
tools/docx/make_docx.sh builds/v9.1/paper_v9_1.docx  # Word version
```

## Working with issues

Work items, supervisor and reviewer comments, and author decisions are tracked as GitHub issues.
Templates are in `.github/ISSUE_TEMPLATE/`. To file the initial backlog once: `gh auth login`, then `issues/create_issues.sh`.

Two issues need an author decision before submission: the scope of the manual audit (#1) and the missing
Selection-Matched Text RAG run (#2).

## Release routine for a new version

1. Edit `paper/paper_v9_0_elsarticle.tex` (or work through an issue with the Claude Code kit).
2. Rebuild: `tools/cas/make_cas.sh` and `tools/docx/make_docx.sh`.
3. Copy the outputs to `builds/vX.Y/`, add a CHANGELOG entry, commit with `Closes #n` for the issues it resolves.
4. `git tag -a vX.Y -m "..." && git push --follow-tags`.

#!/usr/bin/env bash
# Build builds/<version>/paper.docx from paper/paper_v9_0_elsarticle.tex.
# Needs: pdflatex (TeX Live), pandoc >= 3, python3. Run from the repository root.
set -euo pipefail
SRC=${SRC:-paper/paper_v9_0_elsarticle.tex}
OUTDOCX=${1:-paper.docx}
( cd "$(dirname "$SRC")" && pdflatex -interaction=nonstopmode "$(basename "$SRC")" >/dev/null && pdflatex -interaction=nonstopmode "$(basename "$SRC")" >/dev/null )
SRC="$SRC" python3 tools/docx/build.py
python3 tools/docx/inline_math.py tools/docx/out/paper_for_docx.tex
pandoc tools/docx/out/paper_for_docx.tex -f latex -t docx --reference-doc=tools/docx/ref_tnr.docx --number-sections -o tools/docx/out/draft.docx
python3 - <<'PY'
import re,subprocess
t=subprocess.run(['pandoc','tools/docx/out/draft.docx','-t','plain','--wrap=none'],capture_output=True,text=True).stdout
k=t.rfind('\nReferences\n'); inc=len(t.split()); exc=len(t[:k].split())
p='tools/docx/out/paper_for_docx.tex'; s=open(p).read()
s=s.replace('WORDCOUNTLINE','\\textbf{Word count:} %s words including references (%s excluding references); text inside figures not included.'%(f'{inc:,}',f'{exc:,}'))
open(p,'w').write(s); print('word count',inc,exc)
PY
pandoc tools/docx/out/paper_for_docx.tex -f latex -t docx --reference-doc=tools/docx/ref_tnr.docx --number-sections -o tools/docx/out/draft.docx
python3 tools/docx/finish.py tools/docx/out/draft.docx "$OUTDOCX"
echo "wrote $OUTDOCX"

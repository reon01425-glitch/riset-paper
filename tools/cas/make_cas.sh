#!/usr/bin/env bash
# Regenerate paper/paper_v9_0_cas_{dc,sc}.tex from the elsarticle content source and compile them.
set -euo pipefail
python3 tools/cas/convert.py cas-dc paper/paper_v9_0_cas_dc.tex
python3 tools/cas/convert.py cas-sc paper/paper_v9_0_cas_sc.tex
cd paper
for f in paper_v9_0_cas_dc paper_v9_0_cas_sc; do for i in 1 2 3; do pdflatex -interaction=nonstopmode $f.tex >/dev/null; done; echo "built paper/$f.pdf"; done

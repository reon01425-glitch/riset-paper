#!/usr/bin/env python3
"""Split a paper into one file per top-level section, and merge it back.

  python3 sections.py split paper.tex work/iter1      # writes 00_preamble.tex, 01_*.tex ..., 99_back.tex
  python3 sections.py merge work/iter1 paper_new.tex  # concatenates the files in name order

Each section file starts at its \\section{...} line, so parallel agents can each
own one file without touching the others. The back matter (from
\\section*{Acknowledgements} on) and the preamble/front matter are kept as
separate files that agents should not edit.
"""
import os, re, sys

def slug(t):
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40]

def split(tex, out):
    s = open(tex, encoding="utf-8").read()
    back_i = s.find("\\section*{Acknowledgements}")
    if back_i < 0:
        back_i = s.find("\\begin{thebibliography}")
    heads = [m for m in re.finditer(r"^\\section\{([^}]*)\}", s, re.M) if m.start() < back_i]
    os.makedirs(out, exist_ok=True)
    first = heads[0].start() if heads else back_i
    open(os.path.join(out, "00_preamble.tex"), "w", encoding="utf-8").write(s[:first])
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else back_i
        name = f"{i + 1:02d}_{slug(m.group(1))}.tex"
        open(os.path.join(out, name), "w", encoding="utf-8").write(s[m.start():end])
        print(f"{name}\t{len(s[m.start():end].split())} tokens")
    open(os.path.join(out, "99_back.tex"), "w", encoding="utf-8").write(s[back_i:])

def merge(d, out):
    parts = sorted(f for f in os.listdir(d) if re.match(r"^\d\d_.*\.tex$", f))
    with open(out, "w", encoding="utf-8") as fo:
        for f in parts:
            fo.write(open(os.path.join(d, f), encoding="utf-8").read())
    print(f"merged {len(parts)} files -> {out}")

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("split", "merge"):
        sys.exit(__doc__)
    (split if sys.argv[1] == "split" else merge)(sys.argv[2], sys.argv[3])

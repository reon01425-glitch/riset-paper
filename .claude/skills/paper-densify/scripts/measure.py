#!/usr/bin/env python3
"""Measure a LaTeX paper the way a journal checker sees it.

Usage:
  python3 measure.py paper.tex                       # preprint layout as written
  python3 measure.py paper.tex --layout twocol       # Elsevier final 5p two-column
  python3 measure.py paper.tex --baseline old.pdf    # also report numbers that disappeared
  python3 measure.py paper.tex --json                # machine-readable output

Reports: total pages, pages before References, words excluding references
(pdftotext, includes table and figure text, which checkers also count),
words per section, floats defined vs cited, Type 3 (bitmap) fonts,
Overfull boxes, undefined references, and numbers lost vs a baseline PDF.
Needs: pdflatex, pdftotext, pdffonts (TeX Live + poppler).
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

def make_twocol(src):
    s = src.replace("\\documentclass[preprint,10pt]{elsarticle}",
                    "\\documentclass[final,5p,twocolumn]{elsarticle}")
    s = re.sub(r"\\begin\{(figure|table)\}\[[^\]]*\]", r"\\begin{\1*}[!t]", s)
    s = re.sub(r"\\end\{(figure|table)\}", r"\\end{\1*}", s)
    return s

def compile_pdf(tex_path, layout):
    d = os.path.dirname(os.path.abspath(tex_path))
    name = os.path.splitext(os.path.basename(tex_path))[0]
    work = tempfile.mkdtemp(prefix="measure_")
    for item in os.listdir(d):
        p = os.path.join(d, item)
        if item.startswith("measure_"):
            continue
        if os.path.isdir(p):
            shutil.copytree(p, os.path.join(work, item), dirs_exist_ok=True)
        else:
            shutil.copy2(p, work)
    src = open(tex_path, encoding="utf-8").read()
    if layout == "twocol":
        src = make_twocol(src)
    open(os.path.join(work, name + ".tex"), "w", encoding="utf-8").write(src)
    log = ""
    for _ in range(3):
        r = run(["pdflatex", "-interaction=nonstopmode", name + ".tex"], work)
        log = r.stdout
    return os.path.join(work, name + ".pdf"), log, work

def pdf_text(pdf, first=None, last=None):
    cmd = ["pdftotext"]
    if first: cmd += ["-f", str(first)]
    if last: cmd += ["-l", str(last)]
    cmd += [pdf, "-"]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def n_pages(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else 0

def refs_start_page(pdf, pages):
    for p in range(1, pages + 1):
        if re.search(r"^References\s*$", pdf_text(pdf, p, p), re.M):
            return p
    return None

def body_text(pdf):
    t = pdf_text(pdf)
    m = list(re.finditer(r"^References\s*$", t, re.M))
    if m:
        return t[:m[-1].start()]
    k = t.rfind("\n[1] ")
    return t[:k] if k > 0 else t

def section_words(text):
    out, cur, buf = [], "front matter", []
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r"^\d+(\.\d+)?\.\s+[A-Z][^.]{2,90}$", s) and len(s.split()) <= 14:
            out.append((cur, len(" ".join(buf).split())))
            cur, buf = s, []
        else:
            buf.append(line)
    out.append((cur, len(" ".join(buf).split())))
    return out

def floats_report(tex):
    labels = re.findall(r"\\label\{((?:fig|tab|alg):[^}]+)\}", tex)
    uncited = [l for l in labels if not re.search(r"\\(?:ref|cref|autoref)\{" + re.escape(l) + r"\}", tex)]
    figs = len(re.findall(r"\\begin\{figure\*?\}", tex))
    tabs = len(re.findall(r"\\begin\{table\*?\}", tex))
    return {"figures": figs, "tables": tabs, "uncited": uncited}

def numbers(text):
    return set(re.findall(r"(?<![\w.])\d+(?:[.,]\d+)+(?![\w])", text))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--layout", choices=["asis", "twocol"], default="asis")
    ap.add_argument("--baseline", help="older PDF; report decimal numbers that disappeared")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    tex = open(a.tex, encoding="utf-8").read()
    pdf, log, work = compile_pdf(a.tex, a.layout)
    if not os.path.exists(pdf):
        print("COMPILE FAILED\n" + "\n".join(l for l in log.split("\n") if l.startswith("!"))[:2000])
        sys.exit(1)
    pages = n_pages(pdf)
    rp = refs_start_page(pdf, pages)
    body = body_text(pdf)
    fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
    rep = {
        "layout": a.layout,
        "pages_total": pages,
        "references_start_page": rp,
        "pages_without_references": (rp - 1) if rp else None,
        "words_excluding_references": len(body.split()),
        "words_including_references": len(pdf_text(pdf).split()),
        "sections": section_words(body),
        "floats": floats_report(tex),
        "type3_fonts": fonts.count("Type 3"),
        "overfull_boxes": len(re.findall(r"Overfull \\hbox", log)),
        "undefined_refs": len(re.findall(r"Reference `[^']+' on page \d+ undefined", log)),
        "errors": [l for l in log.split("\n") if l.startswith("!")][:10],
        "pdf": pdf,
    }
    if a.baseline:
        old = numbers(body_text(a.baseline))
        rep["numbers_lost_vs_baseline"] = sorted(old - numbers(body))
        rep["numbers_new_vs_baseline"] = sorted(numbers(body) - old)
    if a.json:
        print(json.dumps(rep, indent=1, ensure_ascii=False)); return
    print(f"layout: {rep['layout']}  pages: {pages}  references start: p{rp}  "
          f"pages w/o refs: {rep['pages_without_references']}")
    print(f"words excl. references: {rep['words_excluding_references']}  incl. references: {rep['words_including_references']}")
    print(f"figures: {rep['floats']['figures']}  tables: {rep['floats']['tables']}  "
          f"uncited floats: {rep['floats']['uncited'] or 'none'}")
    print(f"type3 fonts: {rep['type3_fonts']}  overfull: {rep['overfull_boxes']}  "
          f"undefined refs: {rep['undefined_refs']}  errors: {len(rep['errors'])}")
    print("words per section:")
    for n, c in rep["sections"]:
        print(f"  {c:5d}  {n[:70]}")
    if a.baseline:
        print("numbers lost vs baseline:", rep["numbers_lost_vs_baseline"] or "none")
        print("numbers new vs baseline:", rep["numbers_new_vs_baseline"] or "none")
    print("pdf:", pdf)

if __name__ == "__main__":
    main()

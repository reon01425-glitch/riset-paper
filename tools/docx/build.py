#!/usr/bin/env python3
"""Build a Word (.docx) version of the paper from v86.tex (= v9.0 content).

Text, headings, lists, equations (OMML) and tables stay editable; TikZ/pgfplots
figures and the algorithm are rendered to 300-dpi PNG with the same LaTeX code.
"""
import os, re, subprocess, shutil

# usage: compile paper/paper_v9_0_elsarticle.tex once (for its .aux), then
#   python3 tools/docx/build.py && python3 tools/docx/inline_math.py tools/docx/out/paper_for_docx.tex
#   pandoc tools/docx/out/paper_for_docx.tex -f latex -t docx --reference-doc=tools/docx/ref_tnr.docx --number-sections -o draft.docx
#   python3 tools/docx/finish.py draft.docx paper.docx
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
SRC = os.environ.get('SRC', os.path.join(ROOT, 'paper', 'paper_v9_0_elsarticle.tex'))
AUX = os.environ.get('AUX', SRC[:-4] + '.aux')
TAB = os.path.join(os.path.dirname(SRC), 'paper_tables')
OUT = os.path.join(HERE, 'out')
FIG = os.path.join(OUT, 'figs')
os.makedirs(FIG, exist_ok=True)

s = open(SRC, encoding='utf-8').read()
numbers_tex = open(os.path.join(TAB, 'numbers.tex')).read()
macros = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', numbers_tex))

# ---------- label numbers from the LaTeX run ----------
labels = {}
for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', open(AUX).read()):
    labels[m.group(1)] = m.group(2)

def balanced(text, i):
    """text[i] == '{' -> index after matching '}'"""
    depth = 0
    for j in range(i, len(text)):
        if text[j] == '{': depth += 1
        elif text[j] == '}':
            depth -= 1
            if depth == 0: return j + 1
    raise ValueError('unbalanced')

def take_cmd(text, name):
    """remove first \\name{...}; return (arg, text_without)"""
    k = text.find('\\' + name + '{')
    if k < 0: return None, text
    a = k + len(name) + 1
    b = balanced(text, a)
    return text[a + 1:b - 1], text[:k] + text[b:]

# ---------- bibliography -> numbered list, citations -> [n] ----------
bib_i = s.index('\\begin{thebibliography}'); bib_j = s.index('\\end{thebibliography}')
bib = s[bib_i:bib_j]
items = re.split(r'\\bibitem\{([^}]+)\}', bib)[1:]
keys = items[0::2]; texts = [t.strip() for t in items[1::2]]
num = {k: i + 1 for i, k in enumerate(keys)}

def cite_sub(m):
    ns = sorted(num[k.strip()] for k in m.group(1).split(','))
    return '[' + ', '.join(map(str, ns)) + ']'

# ---------- pieces of the document ----------
title = re.search(r'\\title\{(.*?)\}\n', s).group(1)
abstract = re.search(r'\\begin\{abstract\}\n(.*?)\n\\end\{abstract\}', s, re.S).group(1)
keywords = re.search(r'\\begin\{keyword\}\n(.*?)\n\\end\{keyword\}', s, re.S).group(1).replace(' \\sep ', '; ')
body = s[s.index('\\section{Introduction}'):bib_i]
body = body.replace('\\small\n\\setlength{\\bibsep}{2pt}\n', '')

# inline \input tables
body = re.sub(r'\\input\{paper_tables/([\w_]+)\.tex\}',
              lambda m: open(os.path.join(TAB, m.group(1) + '.tex')).read(), body)

PRE = r"""\documentclass[border=4pt]{standalone}
\input{glyphtounicode}\pdfgentounicode=1
\usepackage[T1]{fontenc}\usepackage{lmodern}
\usepackage{amsmath,amssymb,graphicx,xcolor,booktabs,array}
\usepackage{algorithm,algorithmic}
\usepackage{tikz}\usetikzlibrary{positioning,arrows.meta,fit,backgrounds}
\usepackage{pgfplots}\pgfplotsset{compat=1.18}
\newif\ifshoworacle\showoracletrue
\newcommand{\nVerified}{40}
\newlength{\figw}\setlength{\figw}{16cm}
\begin{document}
"""

def render(label, inner):
    inner = inner.replace('\\centering', '')
    inner = re.sub(r'\\eqref\{([^}]+)\}', lambda m: '(' + labels[m.group(1)] + ')', inner)
    inner = re.sub(r'\\ref\{([^}]+)\}', lambda m: labels[m.group(1)], inner)
    for w in ('\\textwidth', '\\columnwidth', '\\linewidth'):
        inner = inner.replace(w, '\\figw')
    tex = PRE + inner + '\n\\end{document}\n'
    base = os.path.join(FIG, label.replace(':', '_'))
    open(base + '.tex', 'w').write(tex)
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', FIG, base + '.tex'],
                       capture_output=True, text=True)
    if not os.path.exists(base + '.pdf'):
        raise SystemExit('render failed ' + label + '\n' + r.stdout[-1500:])
    subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', base + '.pdf', base], check=True)
    return base + '.png'

def clean_caption(c):
    c = re.sub(r'Eq\.~\\eqref\{([^}]+)\}', lambda m: 'Eq. (' + labels[m.group(1)] + ')', c)
    c = re.sub(r'\\ref\{([^}]+)\}', lambda m: labels[m.group(1)], c)
    return c

def float_sub(m):
    env, inner = m.group(1), m.group(3)
    lab = re.search(r'\\label\{([^}]+)\}', inner).group(1)
    cap, inner = take_cmd(inner, 'caption')
    inner = re.sub(r'\\label\{[^}]+\}', '', inner)
    cap = clean_caption(cap)
    n = labels[lab]
    if env == 'table':
        inner = inner.replace('\\centering', '').replace('\\small', '').replace('\\scriptsize', '')
        inner = re.sub(r'\\setlength\{\\tabcolsep\}\{[^}]*\}', '', inner)
        # strip \resizebox{..}{!}{% ... }
        k = inner.find('\\resizebox')
        if k >= 0:
            a = inner.index('{!}{', k) + 3
            b = balanced(inner, a)
            inner = inner[:k] + inner[a + 1:b - 1] + inner[b:]
        # tabularx -> tabular
        inner = re.sub(r'\\begin\{tabularx\}\{[^}]*\}', r'\\begin{tabular}', inner)
        inner = inner.replace('\\end{tabularx}', '\\end{tabular}')
        inner = re.sub(r'>\{\\raggedright\\arraybackslash\}', '', inner)
        inner = re.sub(r'p\{[\d.]+cm\}', 'l', inner).replace('{lX}', '{ll}').replace(' X}', ' l}').replace('X}', 'l}')
        inner = re.sub(r'^%.*$', '', inner, flags=re.M)
        return '\n\\begin{table}\n\\caption{Table %s. %s}\n%s\n\\end{table}\n' % (n, cap, inner.strip())
    if env == 'algorithm':
        png = render(lab, '\\begin{minipage}{15cm}\n' + inner + '\n\\end{minipage}')
        return '\n\\begin{figure}\n\\includegraphics{%s}\n\\caption{Algorithm %s. %s}\n\\end{figure}\n' % (png, n, cap)
    png = render(lab, inner)
    return '\n\\begin{figure}\n\\includegraphics{%s}\n\\caption{Fig. %s. %s}\n\\end{figure}\n' % (png, n, cap)

body = re.sub(r'\\begin\{(figure|table|algorithm)\}(\[[^\]]*\])(.*?)\\end\{\1\}', float_sub, body, flags=re.S)

def resolve(t):
    t = re.sub(r'\\cite[pt]?\{([^}]+)\}', cite_sub, t)
    t = re.sub(r'Eq\.~\\eqref\{([^}]+)\}', lambda m: 'Eq. (' + labels[m.group(1)] + ')', t)
    t = re.sub(r'\\eqref\{([^}]+)\}', lambda m: '(' + labels[m.group(1)] + ')', t)
    t = re.sub(r'\\ref\{([^}]+)\}', lambda m: labels[m.group(1)], t)
    t = t.replace('[leftmargin=*]', '')
    for k, v in macros.items():
        t = t.replace('\\' + k + '{}', v).replace('\\' + k + ' ', v + ' ')
    return t

body = resolve(body)
# equation numbers: append (n) inside each numbered display
eqn = [0]
def eq_sub(m):
    eqn[0] += 1
    inner = re.sub(r'\\label\{[^}]+\}', '', m.group(1)).rstrip().rstrip(',.')
    tail = m.group(1).rstrip()[-1] if m.group(1).rstrip()[-1] in ',.' else ''
    return '\\[\n%s%s \\qquad (%d)\n\\]' % (inner.strip(), tail, eqn[0])
body = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', eq_sub, body, flags=re.S)

refs = '\n\\section*{References}\n' + '\n\n'.join('[%d] %s' % (i + 1, t) for i, t in enumerate(texts)) + '\n'

authors = (r"Cipta Fikri Wiratama\textsuperscript{a}, Indra Waspada\textsuperscript{a,*}, Dhena Kamalia Fu'adi\textsuperscript{a}, "
           r"Ramona Ramli\textsuperscript{b,*}, Henri Tantyoko\textsuperscript{a}, Sandy Kurniawan\textsuperscript{a}, "
           r"Satriawan Rasyid Purnama\textsuperscript{a}")
front = r"""\documentclass{article}
\begin{document}
\title{%s}
\maketitle

%s

\textsuperscript{a} Department of Informatics, Faculty of Science and Mathematics, Universitas Diponegoro, Semarang 50275, Indonesia

\textsuperscript{b} School of Computer Sciences, Universiti Sains Malaysia, 11800 USM, Pulau Pinang, Malaysia

\textsuperscript{*} Corresponding authors: indrawaspada@lecturer.undip.ac.id (I. Waspada); ramona@usm.my (R. Ramli). E-mail of first author: fikriw@students.undip.ac.id

\section*{Abstract}
%s

\textbf{Keywords:} %s

WORDCOUNTLINE

""" % (title, authors, resolve(abstract), keywords)

doc = front + body + refs + '\\end{document}\n'
doc = doc.replace('\\maketitle', '')
open(os.path.join(OUT, 'paper_for_docx.tex'), 'w', encoding='utf-8').write(doc)
print('figures rendered:', len([f for f in os.listdir(FIG) if f.endswith('.png')]))

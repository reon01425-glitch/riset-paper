import re,sys
# usage: python3 tools/cas/convert.py cas-dc|cas-sc OUT.tex [SOURCE_elsarticle.tex]
import os
HERE=os.path.dirname(os.path.abspath(__file__))
src=open(sys.argv[3] if len(sys.argv)>3 else os.path.join(HERE,'..','..','paper','paper_v9_0_elsarticle.tex')).read()
cls=sys.argv[1] if len(sys.argv)>1 else 'cas-dc'
out=sys.argv[2] if len(sys.argv)>2 else 'paper_v9_0_cas_dc.tex'
twocol = cls=='cas-dc'
abstract=re.search(r'\\begin\{abstract\}.*?\\end\{abstract\}',src,re.S).group(0)
keywords=re.search(r'\\begin\{keyword\}\n(.*?)\n\\end\{keyword\}',src,re.S).group(1)
wc='7,139 words including references (6,402 excluding references)'
body=src[src.index('%% ===================================================================\n\\section{Introduction}'):]
# drop CRediT section (replaced by \credit + \printcredits)
i=body.index('\\section*{CRediT authorship contribution statement}'); j=body.index('\\section*{Ethics statement}')
body=body[:i]+'\\printcredits\n\n'+body[j:]
H=r"""\documentclass[a4paper,fleqn]{%s}

%% Unicode map for ligatures, so PDF text extraction (and journal checkers) read fi/fl correctly.
\input{glyphtounicode}
\pdfgentounicode=1

\usepackage[numbers,sort&compress]{natbib}
\usepackage{tabularx}
\usepackage{url}
\usepackage{enumitem}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,fit,backgrounds}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\newif\ifshoworacle
\showoracletrue %% set \showoraclefalse to hide Selection-Matched values in the figures

\setlength{\emergencystretch}{3em}
%% The class always prints an `ORCID(s):' footnote; add orcid=... to each \\author[..]{..}[orcid=...] and delete this line.
\RenewDocumentCommand{\printorcid}{}{}
\renewcommand{\sfdefault}{lmss}

\begin{document}
\let\WriteBookmarks\relax
\def\floatpagepagefraction{1}
\def\textpagefraction{.001}

\input{paper_tables/numbers.tex}

\shorttitle{Procedure selection versus workflow structuring in local RAG}
\shortauthors{C.F. Wiratama et al.}

\title[mode = title]{Procedure Selection versus Workflow Structuring in Local RAG for Institutional SOP Question Answering: An Ablation Study}

\author[1]{Cipta Fikri Wiratama}
\ead{fikriw@students.undip.ac.id}
\credit{Conceptualization, Methodology, Software, Data curation, Validation, Investigation, Writing -- original draft}

\author[1]{Indra Waspada}
\cormark[1]
\ead{indrawaspada@lecturer.undip.ac.id}
\credit{Conceptualization, Supervision, Writing -- review \& editing}

\author[1]{Dhena Kamalia Fu'adi}
\credit{Data curation, Validation, Writing -- review \& editing}

\author[2]{Ramona Ramli}
\cormark[1]
\ead{ramona@usm.my}
\credit{Conceptualization, Methodology, Supervision, Writing -- review \& editing}

\author[1]{Henri Tantyoko}
\credit{Methodology, Validation, Writing -- review \& editing}

\author[1]{Sandy Kurniawan}
\credit{Supervision, Methodology, Writing -- review \& editing}

\author[1]{Satriawan Rasyid Purnama}
\credit{Validation, Formal analysis, Writing -- review \& editing}

\affiliation[1]{organization={Department of Informatics, Faculty of Science and Mathematics, Universitas Diponegoro},
            city={Semarang},
            postcode={50275},
            country={Indonesia}}

\affiliation[2]{organization={School of Computer Sciences, Universiti Sains Malaysia},
            city={Pulau Pinang},
            postcode={11800 USM},
            country={Malaysia}}

\cortext[1]{Corresponding authors}

\nonumnote{Word count: %s.}

%s

%% Highlights are submitted as a separate file (highlights.txt) to keep the manuscript word count down.
%% Uncomment to include them in the manuscript instead.
%%\begin{highlights}
%%\item ...
%%\end{highlights}

\begin{keywords}
%s
\end{keywords}

\maketitle

""" % (cls, wc, abstract, keywords)
body=body.replace("\\RETURN $\\textsc{GenerateLocalLLM}(\\textsc{PromptTemplate}(W \\,\\|\\, C, q))$","\\RETURN $\\textsc{Generate}(\\textsc{Prompt}(W \\,\\|\\, C, q))$")
doc=H+body
doc=doc.replace("\\textbf{Background:}","\\noindent\\textbf{Background:}")
WIDE_FIG={'fig:sopdoc','fig:actors','fig:arch','fig:graphs','fig:prompt','fig:tradeoff'}
WIDE_TAB={'tab:positioning','tab:errormap','tab:systems','tab:results','tab:percat','tab:selection'}
def conv(m):
    env,opt,inner=m.group(1),m.group(2),m.group(3)
    lab=re.search(r'\\label\{([^}]+)\}',inner); lab=lab.group(1) if lab else ''
    wide = twocol and (lab in WIDE_FIG or lab in WIDE_TAB)
    if twocol and not wide:
        inner=inner.replace('\\textwidth','\\columnwidth')
        if lab in ('fig:forest','fig:embedding'):
            inner=inner.replace('\\begin{tikzpicture}','\\resizebox{\\columnwidth}{!}{%\n\\begin{tikzpicture}',1).replace('\\end{tikzpicture}','\\end{tikzpicture}}',1)
    e = env+'*' if wide else env
    pos = '[!t]' if wide else '[!htbp]'
    return '\\begin{%s}%s%s\\end{%s}'%(e,pos,inner,e)
doc=re.sub(r'\\begin\{(figure|table)\}(\[[^\]]*\])(.*?)\\end\{\1\}',conv,doc,flags=re.S)
open(out,'w').write(doc)
print('wrote',out)

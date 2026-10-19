# Cara pakai (Claude Code)

## 1. Siapkan repo (sekali saja)

```bash
git clone --recurse-submodules <url-repo-ini> && cd <repo>
# kebutuhan: MacTeX (pdflatex + lmodern), poppler (pdftotext, pdffonts), pandoc (untuk .docx)
brew install poppler pandoc
python3 .claude/skills/paper-densify/scripts/measure.py paper/paper_v9_0_cas_dc.tex
```

Kalau perintah terakhir mencetak jumlah halaman dan kata, kit sudah siap.

## 2. Prompt yang ditempel di Claude Code

```
/paper-densify TEX=paper/paper_v9_0_cas_dc.tex DATA=code LAYOUT=asis

Context: this is my ablation paper on procedure selection vs workflow structuring for SOP question
answering (read CLAUDE.md first). My supervisor says good papers are written simply and the paper
should be about 15 pages including references, so 8-13 pages without references in the CAS double-column
layout the paper already uses; the journal checker wants 6,000-7,500 words including the reference list. The current draft still wanders:
results are repeated across sections and some paragraphs do not serve any research question.

Goal for this run:
1. Every paragraph dense and on-topic per style_rules.md; one clear line from problem -> method ->
   ablation -> results -> implication.
2. Add up to 3 new figures or tables, only from repository data, each replacing prose
   (good sources: scores_per_query.csv and generations.jsonl for per-question views).
3. Stay inside 11-12 pages without references (the file is already two-column, so measure with LAYOUT=asis) and at most about 7,300 words including references.

Run the subagents in parallel as the skill describes, iterate until the targets pass (max 3
iterations), save each version as a new file (v9_1, v9_2, ...), and finish with the report table.
Do not change any number unless the number-auditor shows it is wrong, and list the two open author
decisions from CLAUDE.md instead of resolving them.
```

## 3. Setelah selesai
- Buka PDF versi terakhir, cek figure baru satu per satu.
- Baca daftar "numbers lost vs baseline" di laporan akhir: semua harus disengaja.
- Dua keputusan (audit 14/60 dan hasil SOP-Oracle) tetap keputusanmu dan Pak Indra.

---
title: "[decision] Manual audit: paper reports 60 rows, repository shows 14 reviewed"
labels: decision, data-integrity, priority-high
---
**Question:** Which audit numbers does the paper report?

**Evidence**
- Paper (v8.2 to v9.0, Section 5.6 and Table 6): 60/60 rows, agreement 0.983 (kappa 0.955) for step detection, 0.933 (kappa 0.835) for actors.
- `code/results/full_v3_20261008/audit_agreement.json` and commit 4163ed8: only rows 1 to 14 were reviewed; agreement 0.857, kappa not informative; rows 15 to 60 were reset to pending; two rows (naive / CUTI-P2 steps 4 to 5) are flagged for re-checking.
- The values 0.983 / 0.955 / 0.933 / 0.835 do not appear in any repository file.

**Options**
1. Finish the remaining 46 rows, recompute with `audit_agreement.py`, and update the paper with the real values.
2. Report 14/60 honestly and weaken the reliability claim in Sections 5.6 and 7.2.

**Done when:** paper text, Table 6, and `audit_agreement.json` agree.

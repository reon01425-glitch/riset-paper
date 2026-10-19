#!/usr/bin/env bash
# Create the labels and the issues in issues/*.md on the current GitHub repo.
# Needs the GitHub CLI logged in (gh auth login). Run once from the repository root.
set -euo pipefail
# works with the bash 3.2 that ships with macOS
for pair in decision:d93f0b data-integrity:b60205 priority-high:e11d21 task:1d76db writing:5319e7 \
            submission:0e8a16 figure:c5def5 review:fbca04 journal-checker:f9d0c4 analysis:0052cc \
            experiment:006b75 cross-repo:bfdadc infrastructure:cccccc; do
  gh label create "${pair%%:*}" --color "${pair##*:}" --force >/dev/null
done
for f in issues/[0-9]*.md; do
  title=$(sed -n 's/^title: "\(.*\)"$/\1/p' "$f")
  labels=$(sed -n 's/^labels: //p' "$f" | tr -d ' ')
  body=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$f")
  gh issue create --title "$title" --label "$labels" --body "$body"
done

# /draft-paper

Draft all sections of the paper in parallel, then assemble.

## What This Does

Coordinates multiple section-writing agents to draft the complete paper,
then assembles everything into a compilable LaTeX document.

## Prerequisites

Before running, verify `workspace/current-paper.md` shows:
- [x] Literature review complete
- [x] Paper outline complete

If not, stop and ask the user to run `/literature-search` first.

## Parallel Drafting Strategy

Spawn three section-writing agents simultaneously:

**Agent 1 — `intro-writer`:**
Write `workspace/sections/abstract.tex` and `workspace/sections/introduction.tex`

**Agent 2 — `technical-writer`:**
Write:
- `workspace/sections/related_work.tex`
- `workspace/sections/background.tex` (if needed per outline)
- `workspace/sections/methodology.tex`
- `workspace/sections/appendix_proofs.tex`

**Agent 3 — `empirics-writer`:**
Write:
- `workspace/sections/experiments.tex` (ML) or `workspace/sections/empirics.tex` (econ)
- `workspace/sections/appendix_experiments.tex`

After all three complete:

**Agent 4 — `technical-writer`:**
Write `workspace/sections/conclusion.tex`
(conclusion should reference what was actually written in other sections)

## Post-Drafting Steps

After all sections are drafted:

1. Run `citation-manager` to clean and verify all citations
2. Run `latex-assembler` to produce `papers/<slug>/main.tex`
3. Attempt compilation and report results to user

## Reporting

After assembly, tell the user:
- Total page count
- Any sections that need human input (figures, actual experimental results, etc.)
- Any compilation errors
- Suggested next step: `/review-paper` or `/camera-ready`

## Notes on Placeholder Content

The drafts will contain placeholders for:
- `% TODO: INSERT FIGURE` — actual figure files needed
- `% TODO: INSERT ACTUAL RESULTS` — real numbers from experiments
- `% TODO: PROOF NEEDED` — theoretical claims requiring proof

These are intentional. The agents write the structure and prose around real content.

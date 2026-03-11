# /draft-paper

Draft all sections of the paper in parallel, then assemble.

## What This Does

Coordinates multiple section-writing agents to draft the complete paper,
then assembles everything into a compilable LaTeX document.

## Prerequisites

Read `paper/state.yaml` and verify the active target's stage is at least `outlining`.
If not, stop and ask the user to run `/literature-search` first.

Read `paper/<active_target>/outline.md` to confirm the outline exists.

## Parallel Drafting Strategy

Spawn three section-writing agents simultaneously:

**Agent 1 — `intro-writer`:**
Write `paper/<active_target>/sections/abstract.tex` and `paper/<active_target>/sections/introduction.tex`

**Agent 2 — `technical-writer`:**
Write:
- `paper/<active_target>/sections/related_work.tex`
- `paper/<active_target>/sections/background.tex` (if needed per outline)
- `paper/<active_target>/sections/methodology.tex`
- `paper/<active_target>/sections/appendix_proofs.tex`

**Agent 3 — `empirics-writer`:**
Write:
- `paper/<active_target>/sections/experiments.tex` (ML) or `paper/<active_target>/sections/empirics.tex` (econ)
- `paper/<active_target>/sections/appendix_experiments.tex`

After all three complete:

**Agent 4 — `technical-writer`:**
Write `paper/<active_target>/sections/conclusion.tex`
(conclusion should reference what was actually written in other sections)

## Post-Drafting Steps

After all sections are drafted:

1. Run `citation-manager` to audit `paper/<active_target>/sections/*.tex` and produce `paper/<active_target>/references.bib`
2. Run `latex-assembler` with template from `.pepper/templates/<venue>/` to produce `paper/<active_target>/main.tex`
3. Attempt compilation and report results to user
4. Update `paper/state.yaml` to set the active target's stage to `drafting`

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

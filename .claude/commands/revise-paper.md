# /revise-paper

Revise the paper based on review feedback, then re-assemble.

## What This Does

Takes review feedback (from peer review, actual reviewers, or your own notes), produces a
structured revision plan, selectively invokes writer agents to make changes, and re-assembles
the paper.

## Input Resolution

`$ARGUMENTS` can be:
- **Inline text** — treat as review feedback directly
- **A file path** — read the file as review feedback
- **Empty** — default to `paper/<active_target>/review.md` (output from `/review-paper`)

If the resolved input does not exist or is empty, stop and ask the user to provide review
feedback or run `/review-paper` first.

## Prerequisites

1. Read `paper/state.yaml` to get the active target and current stage.
2. Verify stage is at least `drafting`. If not, tell the user to run `/draft-paper` first.
3. Verify that section files exist in `paper/<active_target>/sections/`.

## Revision Flow

### Step 1: Determine Round Number
Scan `paper/<active_target>/revisions/` for directories matching `round-<N>`. Set the new
round to N+1 (or 1 if no prior rounds exist).

### Step 2: Save Review Input
Create `paper/<active_target>/revisions/round-<N>/review-input.md` with the resolved
review feedback.

### Step 3: Backup Current Sections
Copy all `.tex` files from `paper/<active_target>/sections/` to
`paper/<active_target>/revisions/round-<N>/sections-before/`.

### Step 4: Generate Revision Plan
Invoke the `revision-planner` agent. It reads the review input and current sections,
then produces `paper/<active_target>/revisions/round-<N>/revision-plan.md`.

### Step 5: Present Plan and Confirm
Show the user:
- Summary of revision strategy
- Per-section action breakdown (which sections change, which don't)
- Any prerequisites (new results needed, etc.)
- Any conflicts with claims.md

Ask: "Shall I proceed with this revision plan? You can also ask me to modify it first."

Wait for user confirmation before proceeding.

### Step 6: Invoke Writers Selectively
Based on the revision plan, invoke ONLY the agents that have assigned work:
- `intro-writer` — if abstract.tex or introduction.tex need changes
- `technical-writer` — if related_work.tex, background.tex, methodology.tex, theory.tex,
  appendix_proofs.tex, or conclusion.tex need changes
- `empirics-writer` — if experiments.tex, empirics.tex, or appendix_experiments.tex need changes

Run agents in parallel where possible (intro-writer and empirics-writer can run in parallel;
technical-writer can run in parallel with the others).

### Step 7: Re-Assemble
1. Run `citation-manager` to update references
2. Run `latex-assembler` to produce updated `main.tex`
3. Attempt compilation and note any errors

### Step 8: Generate Changelog
Create `paper/<active_target>/revisions/round-<N>/changelog.md` summarizing:
- Which sections were modified
- Key changes made (bulleted list)
- Any remaining TODOs or unresolved items

### Step 9: Update State
In `paper/state.yaml`:
- Set the active target's stage to `drafting` (ready for another review cycle)
- Set or update `revision_round: <N>` for the active target

## Reporting

After completion, tell the user:
- Revision round number
- Sections revised vs. unchanged
- Compilation status (success/errors)
- Any remaining TODOs or prerequisites that weren't met
- Suggested next step: `/review-paper` to verify the revisions

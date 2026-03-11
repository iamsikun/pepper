# /update-results

Update the paper after results or data change, then re-assemble.

## What This Does

A lighter-weight variant of `/revise-paper` for when experimental results, figures, or data
change — not driven by reviewer feedback. Maps content changes to affected sections and
selectively updates them.

## Input Resolution

`$ARGUMENTS` can be:
- **Inline text** — description of what changed (e.g., "re-ran ablations with new hyperparams,
  results in results/ablations_v2/")
- **A file path** — read the file for a detailed description of changes

If empty, ask the user: "What changed? Please describe the updated results or point me to
the new data/figures."

## Prerequisites

1. Read `paper/state.yaml` to get the active target and current stage.
2. Verify stage is at least `drafting`. If not, tell the user to run `/draft-paper` first.
3. Verify that section files exist in `paper/<active_target>/sections/`.

## Update Flow

### Step 1: Determine Round Number
Scan `paper/<active_target>/revisions/` for directories matching `round-<N>`. Set the new
round to N+1 (or 1 if no prior rounds exist).

### Step 2: Save Update Input
Create `paper/<active_target>/revisions/round-<N>/review-input.md` with the following format:

```markdown
## Update Type: results-update

<user's description of what changed>
```

The `## Update Type: results-update` header tells the revision-planner to focus on mapping
content changes to sections rather than addressing reviewer criticism.

### Step 3: Backup Current Sections
Copy all `.tex` files from `paper/<active_target>/sections/` to
`paper/<active_target>/revisions/round-<N>/sections-before/`.

### Step 4: Generate Revision Plan
Invoke the `revision-planner` agent. It reads the update input (noting the results-update
header) and current sections, then produces
`paper/<active_target>/revisions/round-<N>/revision-plan.md`.

### Step 5: Present Plan and Confirm
Show the user:
- Which sections will be updated
- What changes are planned
- Any sections that reference changed data

Ask: "Shall I proceed with these updates? You can also ask me to modify the plan first."

Wait for user confirmation before proceeding.

### Step 6: Invoke Writers Selectively
Same as `/revise-paper` — invoke only agents with assigned work, in parallel where possible.

### Step 7: Re-Assemble
1. Run `citation-manager` to update references
2. Run `latex-assembler` to produce updated `main.tex`
3. Attempt compilation and note any errors

### Step 8: Generate Changelog
Create `paper/<active_target>/revisions/round-<N>/changelog.md` summarizing:
- Which sections were modified
- Key changes made (bulleted list)
- Updated numbers/figures

### Step 9: Update State
In `paper/state.yaml`:
- Stage stays at `drafting` (no review cycle needed for results updates)
- Set or update `revision_round: <N>` for the active target

## Reporting

After completion, tell the user:
- Revision round number
- Sections updated vs. unchanged
- Compilation status (success/errors)
- Any remaining TODOs
- Suggested next step: `/review-paper` to check the updated paper

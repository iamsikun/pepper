# /create-journal-version

Create a journal version of the paper alongside the conference version.

## What This Does

Sets up a journal target directory with its own outline, sections, and build artifacts,
sharing the research materials from `paper/shared/`.

## Custom Instructions

`$ARGUMENTS` contains optional freeform input from the user.

If non-empty, parse for:
- Target journal venue (e.g., "Management Science", "Econometrica")
- Whether to bootstrap from conference outline (e.g., "based on the conference version")

Examples:
- "Management Science" → use as venue, skip the venue question
- "Econometrica, bootstrap from conference" → set venue and bootstrap preference

If empty, proceed fully interactively as default.

## Instructions

### Step 1: Ask for Journal Venue

Ask the user which journal venue to target (from the journal venues defined in `.pepper/config.yaml`).

### Step 2: Create Directory Structure

```bash
mkdir -p paper/journal/sections
mkdir -p paper/journal/figures
```

### Step 3: Write Target Metadata

**`paper/journal/target.yaml`:**
```yaml
name: journal
venue: <venue name>
template: <venue template key: econometrica, informs>
mode: submission
page_limit: <from venue requirements, or "none">
audience: <econometrics, marketing, management-science, operations>
```

### Step 4: Update State

Add journal entry to `paper/state.yaml`:
```yaml
targets:
  journal:
    stage: init
    created: <today's date>
```

### Step 5: Optionally Bootstrap from Conference

If `paper/conference/outline.md` exists, ask the user:
"A conference outline exists. Would you like to use it as a reference for the journal outline?"

If yes, invoke the `paper-outliner` agent, instructing it to read the conference outline
as reference but write a fresh journal-style outline to `paper/journal/outline.md`.

### Step 6: Set Active Target

Ask the user if they want to switch the active target to journal. If yes, update
`active_target` in `paper/state.yaml` to `journal`.

Confirm: "Journal version created for <venue>. Run `/literature-search` or `/draft-paper` to continue."

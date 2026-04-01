# /import-paper

Import an existing paper (`.tex` + `.bib` files) into the pepper pipeline.
Use this when you have a working paper and want to leverage pepper's review, revision, or venue-retargeting capabilities.

## What This Does

Ingests an existing LaTeX paper into the `paper/` directory structure, reverse-engineers the required state files, decomposes the paper into sections, and enters the pipeline mid-stream.

## Custom Instructions

`$ARGUMENTS` contains optional freeform input from the user.

If non-empty, parse for:
- Path to the paper (e.g., "~/papers/my-draft/main.tex")
- Import mode (e.g., "in review mode", "for revision", "retarget to journal")
- Any combination — use what is provided, ask for the rest

If empty, proceed fully interactively as default.

## Instructions

### Step 1: Check for Existing State

Check if `paper/state.yaml` already exists. If so, **warn the user** and ask whether to
overwrite or abort. Do NOT proceed without confirmation.

### Step 2: Locate Source Files

Ask for the **path to their existing paper** (folder or `.tex` file). Scan for:
- `.tex` files — find the **main file** (contains `\documentclass` and `\begin{document}`)
- `.bib` files
- `.sty` / `.cls` files (for venue auto-detection)
- Figures (`.pdf`, `.png`, `.eps`, `.jpg`) referenced via `\includegraphics{}`

Parse `\input{}` / `\include{}` to build a dependency tree. Present findings for confirmation.

### Step 3: Analyze Paper Structure

Parse the main `.tex` file to extract:
- `\title{}`, `\begin{abstract}`, `\section{}` names/boundaries
- `\bibliography{}` or `\addbibresource{}` → bib files
- `\usepackage{<venue_style>}` → venue hint (match against `.pepper/templates/`)
- `\newcommand` / `\DeclareMathOperator` → custom macros

Classify as **monolithic** (single file) or **multi-file** (`\input{}`/`\include{}`).

### Step 4: Gather User Input (with pre-filled suggestions)

Ask for the same information as `/new-paper` Step 2 (title, topic, contributions, venue,
paper type), pre-filling from what was extracted. Additionally ask for **import mode**:
- **Review** — "I have a complete draft, I want feedback" → stage = `drafting`
- **Revise** — "I want to restructure/rewrite parts" → stage = `outlining`
- **Retarget** — "I want to adapt this for a different venue" → stage = `drafting`

### Step 5: Scan Repo for Source Map

Same as `/new-paper` Step 1 — scan repo tree, classify directories using patterns from
`.pepper/config.yaml` `source_categories`, present for confirmation.

### Step 6: Create Directory Structure + State Files

Same structure as `/new-paper` Steps 3-5, with these additions to `paper/state.yaml`:
- `imported_from: <original paper path>`
- `import_mode: <review/revise/retarget>` under the target
- Stage set per import mode (not `init`)

Add to `paper/shared/context.md` an extra `## Import Notes` section with: imported path,
import mode, original structure (monolithic/multi-file), custom macros list.

### Step 7: Ingest Paper Files

**Bibliography:** Copy/merge all `.bib` files → `paper/shared/references-master.bib` and
`paper/<target>/references.bib`

**Figures:** Copy referenced figures → `paper/<target>/figures/`. Record old→new path mapping.

**Sections — Multi-file:** Match `\section{}` titles to standard names, copy to
`paper/<target>/sections/<name>.tex`. Ask user to classify unrecognized sections.

**Sections — Monolithic:** Split at `\section{}` boundaries. Extract abstract from
`\begin{abstract}`. Extract macros from preamble → `macros.tex` or note in context.md.

**Main file:** Copy original → `paper/<target>/main.tex` as-is initially.

### Step 8: Fix Internal References

- Update `\includegraphics{}` paths to use `figures/` prefix
- Verify `\cite{}` keys exist in imported `.bib` — report missing keys
- Report potentially broken `\ref{}`/`\label{}` references (informational only)

### Step 9: Populate Shared Artifacts from Paper Content

- `paper/shared/claims.md` — extract contributions and theorem/proposition statements
- `paper/shared/figure-plan.md` — inventory `\begin{figure}` with captions and labels
- `paper/shared/table-plan.md` — inventory `\begin{table}` with captions and labels

### Step 10: Generate Retrospective Outline

Invoke `paper-outliner` agent in **retrospective mode**. It reads existing sections and
produces `paper/<target>/outline.md` documenting the current structure.

### Step 11: Confirm

Report: sections imported (with name mappings), references count, figures/tables found,
any issues (unmapped sections, missing figures, broken citations).

**Suggested next step** based on import mode:
- **Review** → "Run `/review-paper` to get feedback on your draft."
- **Revise** → "Edit `paper/<target>/outline.md` to plan restructuring, then `/draft-paper`."
- **Retarget** → "Run `/create-journal-version` to set up the new venue target."

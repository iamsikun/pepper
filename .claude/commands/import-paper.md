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

Examples:
- "paper.tex in review mode" → use paper.tex as source, set review mode, ask for rest
- "~/drafts/pricing/" → use that directory, ask for mode and other details

If empty, proceed fully interactively as default.

## Instructions

### Step 1: Check for Existing State

Check if `paper/` directory and `paper/state.yaml` already exist.
If they do, **warn the user** and ask whether to:
- **Overwrite** — delete existing `paper/` and start fresh
- **Abort** — stop and let the user handle it

Do NOT proceed without user confirmation if state already exists.

### Step 2: Locate Source Files

Ask the user for the **path to their existing paper** (a folder or specific `.tex` file).

Scan that path for:
- **`.tex` files** — find the **main file** (contains `\documentclass` and `\begin{document}`)
- **`.bib` files**
- **`.sty` / `.cls` files** (for venue auto-detection)
- **Figure files** (`.pdf`, `.png`, `.eps`, `.jpg`) referenced via `\includegraphics{}`

Parse `\input{}` / `\include{}` from the main file to build a dependency tree.

Present findings to the user for confirmation:
```
Found paper files:
  Main file: <path>
  Included files: <list>
  Bibliography: <list>
  Style files: <list>
  Figures: <list>
```

### Step 3: Analyze Paper Structure

Parse the main `.tex` file to extract:
- `\title{}` → pre-fill title
- `\begin{abstract}...\end{abstract}` → will become `abstract.tex`
- `\section{}` names and boundaries → section inventory
- `\bibliography{}` or `\addbibresource{}` → locate bib files
- `\usepackage{<venue_style>}` → venue hint (match against templates in `.pepper/templates/`)
- `\newcommand` / `\DeclareMathOperator` / custom macros → preserve list

Classify as:
- **Monolithic** — all content in one `.tex` file
- **Multi-file** — uses `\input{}` / `\include{}` for sections

### Step 4: Gather User Input (with pre-filled suggestions)

Ask the user for the following, pre-filling from what was extracted:

1. **Title** — pre-filled from `\title{}`
2. **Research topic** — 2-3 sentences (user provides)
3. **Key contributions** — attempt to extract from the introduction: look for a paragraph mentioning "contributions" or a bulleted/numbered list; present to user for confirmation/editing
4. **Target venue** — pre-filled if a style package was detected from `.pepper/templates/`, otherwise ask
5. **Paper type** — Methodology / Theory / Empirical / Theory+Experiments
6. **Import mode**:
   - **Review** — "I have a complete draft, I want feedback" → stage will be set to `drafting`
   - **Revise** — "I want to restructure/rewrite parts" → stage will be set to `outlining`
   - **Retarget** — "I want to adapt this for a different venue" → stage will be set to `drafting`

Determine the target name from the venue:
- ML conferences → `conference`
- Journals → `journal`

### Step 5: Scan Repo for Source Map

Same logic as `/new-paper` Step 1 — scan the repo tree, excluding `.git/`, `.claude/`, `.pepper/`, `paper/`, and `node_modules/`.
Classify discovered directories using the category patterns from `.pepper/config.yaml` `source_categories`.
Present to user for confirmation.

### Step 6: Create Directory Structure + State Files

```bash
mkdir -p paper/shared/literature
mkdir -p paper/shared/evidence
mkdir -p paper/<target>/sections
mkdir -p paper/<target>/figures
```

**`paper/state.yaml`:**
```yaml
active_target: <target>
initialized: true
imported_from: <original paper path>
targets:
  <target>:
    stage: <drafting if Review/Retarget, outlining if Revise>
    created: <today's date>
    import_mode: <review/revise/retarget>
```

**`paper/shared/context.md`:**
```markdown
# Paper Context

## Title
<title>

## Topic
<2-3 sentences>

## Contributions
1. <contribution 1>
2. <contribution 2>
3. <contribution 3>

## Paper Type
<type>

## Source Map

The following paths in this repository contain materials relevant to the paper.
Agents should read from these locations when they need project context.

- Documentation: <discovered doc paths>
- Source code: <discovered src paths>
- Experiment results: <discovered results paths>
- Figures: <discovered figure paths>
- Data: <discovered data paths>
- Scripts: <discovered script paths>

## Key Files
<user can annotate important files here>

## Import Notes
- Imported from: <original path>
- Import mode: <review/revise/retarget>
- Original structure: <monolithic/multi-file>
- Custom macros: <list of \newcommand / \DeclareMathOperator definitions, or "none">
```

**`paper/<target>/target.yaml`:**
```yaml
name: <target>
venue: <venue name and year>
template: <venue template key>
mode: blind
page_limit: <from venue requirements>
audience: <ml, econometrics, marketing, management-science, operations>
```

Create empty starter files:
- `paper/shared/claims.md` — with header `# Claims and Evidence`
- `paper/shared/figure-plan.md` — with header `# Figure Plan`
- `paper/shared/table-plan.md` — with header `# Table Plan`

### Step 7: Ingest Paper Files

**Bibliography:**
- Copy/merge all `.bib` files → `paper/shared/references-master.bib`
- Also copy to `paper/<target>/references.bib`

**Figures:**
- Copy all figure files referenced by `\includegraphics{}` → `paper/<target>/figures/`
- Record old-path → new-path mapping for reference fixup later

**Sections — Multi-file case:**
- For each `\input{}`'d file, match its `\section{}` title against `section_name_mapping` from `.pepper/config.yaml`
- Copy to `paper/<target>/sections/<standard_name>.tex`
- If a section title doesn't match any mapping, present it to the user and ask them to classify it (or use a slugified version of the title)
- Preserve any content that doesn't fall into a section (e.g., between `\maketitle` and first `\section{}`) as part of `abstract.tex` or note it

**Sections — Monolithic case:**
- Split the document body at `\section{}` boundaries
- Each section → `paper/<target>/sections/<standard_name>.tex`
- Extract abstract from `\begin{abstract}...\end{abstract}` → `abstract.tex`
- Extract custom macros from preamble → save as `paper/<target>/sections/macros.tex` or note them in `context.md`

**Main file:**
- Copy the original main `.tex` → `paper/<target>/main.tex` as-is initially
- The latex-assembler will reconstruct it properly later if needed

### Step 8: Fix Internal References

- Update `\includegraphics{}` paths in all section files to use the `figures/` prefix
- Verify `\cite{}` keys exist in the imported `.bib` — report any missing keys
- Report any potentially broken `\ref{}` / `\label{}` references (informational, don't fix these automatically)

### Step 9: Populate Shared Artifacts from Paper Content

- **`paper/shared/claims.md`** — Extract contribution bullet points from the introduction and any theorem/proposition statements
- **`paper/shared/figure-plan.md`** — Inventory all `\begin{figure}` environments with their `\caption{}` text and `\label{}` names
- **`paper/shared/table-plan.md`** — Inventory all `\begin{table}` environments with their `\caption{}` text and `\label{}` names

### Step 10: Generate Retrospective Outline

Invoke the `paper-outliner` agent. It will detect existing `.tex` files in `paper/<target>/sections/` and run in **retrospective mode** — reading the imported sections and producing `paper/<target>/outline.md` that documents the current structure.

- If import mode is **Revise**, this outline becomes the starting point for restructuring
- If import mode is **Review** or **Retarget**, the outline documents the current state for reference

### Step 11: Confirm

Report to the user:
- Number of sections imported and their name mappings (original name → standard name)
- Number of references in bibliography
- Number of figures and tables found
- Any issues encountered:
  - Unmapped sections (and how they were handled)
  - Missing figure files
  - Broken `\cite{}` references
- **Suggested next step** based on import mode:
  - **Review** → "Run `/review-paper` to get feedback on your draft."
  - **Revise** → "Edit `paper/<target>/outline.md` to plan your restructuring, then run `/draft-paper`."
  - **Retarget** → "Run `/create-journal-version` to set up the new venue target."

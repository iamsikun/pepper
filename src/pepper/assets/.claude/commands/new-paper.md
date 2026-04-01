# /new-paper

Initialize the paper workspace for this project. Run this first before any other commands.

## What This Does

Scans the repository to discover project materials, captures key information from the user,
and creates the `paper/` directory structure with a source map for all downstream agents.

## Custom Instructions

`$ARGUMENTS` contains optional freeform input from the user.

If non-empty, parse the text for any pre-filled information to reduce interactive prompts:
- Paper title, research topic, contributions, target venue, paper type
- Any combination of these — use what is provided, ask for the rest

Examples:
- "Title: Optimal Pricing with LLMs, Venue: NeurIPS" → pre-fill title and venue, ask for rest
- "ML theory paper on bandit algorithms for dynamic pricing" → infer topic and type, confirm

If empty, proceed fully interactively as default.

## Instructions

### Step 1: Scan the Repository

Scan the repo tree, excluding `.git/`, `.claude/`, `.pepper/`, `paper/`, and `node_modules/`.
Classify discovered directories by name patterns:

| Pattern | Category |
|---|---|
| `docs/`, `notes/`, `writeup/` | Documentation |
| `src/`, `lib/`, `code/` | Source code |
| `results/`, `output/`, `experiments/`, `logs/` | Experiment results |
| `figures/`, `plots/`, `images/`, `viz/` | Figures |
| `data/`, `datasets/` | Data |
| `scripts/`, `bin/` | Scripts |
| `tests/`, `test/` | Tests |

Present the discovered source map to the user for confirmation and edits.

### Step 2: Gather Paper Information

Ask the user for:
1. **Paper Title** (working title is fine)
2. **Research Topic** — 2-3 sentence description
3. **Key Contributions** — 2-4 main claims
4. **Target Venue** — select from venues defined in `.pepper/config.yaml`
5. **Paper Type** — Methodology / Theory / Empirical / Theory+Experiments

Determine the target name from the venue:
- ML conferences → `conference`
- Journals → `journal`

### Step 3: Create Directory Structure

```bash
mkdir -p paper/shared/literature
mkdir -p paper/shared/evidence
mkdir -p paper/<target>/sections
mkdir -p paper/<target>/figures
```

### Step 4: Write State Files

**`paper/state.yaml`:**
```yaml
active_target: <target>
initialized: true
targets:
  <target>:
    stage: init
    created: <today's date>
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
```

**`paper/<target>/target.yaml`:**
```yaml
name: <target>
venue: <venue name and year>
template: <venue template key: neurips, icml, iclr, econometrica, informs>
mode: blind
page_limit: <from venue requirements>
audience: <ml, econometrics, marketing, management-science, operations>
```

### Step 5: Initialize Shared Files

Create empty starter files:
- `paper/shared/claims.md` — with header `# Claims and Evidence`
- `paper/shared/figure-plan.md` — with header `# Figure Plan`
- `paper/shared/table-plan.md` — with header `# Table Plan`
- `paper/shared/references-master.bib` — empty file

### Step 6: Confirm

Tell the user: "Paper workspace initialized. Source map written to `paper/shared/context.md`.
Run `/literature-search` next to begin the literature review."

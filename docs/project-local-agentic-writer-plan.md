# Project-Local Agentic Writer Plan

## Goal

Transform this repository into an installable agentic paper-writing scaffold that
can be dropped into any research project repository and used immediately.

The target user experience is:

1. Run the install script into a project repo.
2. Open Claude Code in that repo.
3. Run `/new-paper` to initialize the paper workspace.
4. Draft and iterate on a conference paper and, optionally, a journal paper.

## Desired End State

The system should model:

- one repository = one research project
- one `paper/` directory = one manuscript family for that project
- up to two paper targets: `paper/conference/` and `paper/journal/`
- shared research truth in `paper/shared/`
- target-specific prose and build artifacts in the target directories

The system should not require:

- `projects/` aliases or symlinks to external repos
- a central hub repo that points at active projects
- plural `papers/` directories
- any project-specific state baked into the scaffold itself

## Core Design Principles

### 1. Project-local by default

Every agent treats the current repository root as the active project. There is no
indirection layer. The repo IS the project.

### 2. Discoverable project context via source map

Research repos have wildly different structures. Some use `src/`, others `code/`.
Some put results in `results/`, others in `output/` or `experiments/`. The system
must not hardcode assumptions about where project materials live.

Instead, `/new-paper` scans the repo and writes a **source map** into
`paper/shared/context.md` that tells all downstream agents where to find things in
THIS specific repo. Agents read the source map rather than guessing paths.

The source map records:

- paths to documentation (e.g., `docs/model.md`, `notes/theory.md`)
- paths to experiment results (e.g., `results/`, `output/analysis/`)
- paths to source code (e.g., `src/`, `lib/`)
- paths to figures (e.g., `figures/`, `plots/`)
- paths to data (e.g., `data/`, `datasets/`)
- any other project-specific locations agents should know about

This is the critical bridge between an arbitrary research repo and the paper-writing
agents.

### 3. One paper program, multiple targets

This is not a "many papers" system. It is one paper program with one or two
publication targets. The main abstraction is:

- shared research inputs and evidence
- conference manuscript output
- journal manuscript output

### 4. Share evidence, not prose

The conference and journal versions share:

- problem framing and claims
- verified evidence and result references
- literature notes and bibliography
- figure and table plans

They maintain separate target-specific section drafts. Never try to share raw
section text between targets.

### 5. Explicit state, minimal magic

Machine-readable YAML files drive the workflow. Pipeline progress is tracked per
target so agents know what has been done and what remains.

### 6. Installable scaffold, not a monolith

This repository is the source template. The install payload is reusable framework
assets (agents, commands, templates, config). It ships zero project-specific state.

## Target Filesystem Layout

### Scaffold files (installed into project repo)

```text
project-root/
├── .claude/
│   ├── agents/                  ← 9 specialized subagent prompts
│   ├── commands/                ← slash command prompts
│   └── settings.json            ← tool permissions
├── .paperwriter/
│   ├── config.yaml              ← system defaults (venue registry, etc.)
│   ├── templates/               ← venue-specific LaTeX templates
│   │   ├── neurips/
│   │   ├── icml/
│   │   ├── iclr/
│   │   ├── econometrica/
│   │   └── informs/
│   └── scripts/
│       └── install.sh           ← installer script
└── CLAUDE.md                    ← system instructions for Claude Code
```

### Runtime files (created by `/new-paper` and subsequent commands)

```text
project-root/
└── paper/
    ├── state.yaml               ← global state: active target, per-target stages
    ├── shared/
    │   ├── context.md           ← title, topic, contributions, source map
    │   ├── claims.md            ← research claims and evidence links
    │   ├── literature/          ← survey markdown files per topic
    │   ├── references-master.bib
    │   ├── figure-plan.md       ← planned figures with descriptions
    │   ├── table-plan.md        ← planned tables with descriptions
    │   └── evidence/            ← verified results, numbers, quotes
    ├── conference/
    │   ├── target.yaml          ← venue, template, mode, page limit, audience
    │   ├── outline.md           ← section-level outline for this target
    │   ├── sections/            ← .tex drafts
    │   ├── figures/             ← target-specific figure files
    │   ├── references.bib       ← subset of master bib for this target
    │   ├── main.tex             ← assembled paper
    │   ├── review.md            ← peer review output
    │   ├── revision-plan.md     ← actionable revision steps
    │   └── camera-ready/        ← submission package
    └── journal/                 ← (optional, same structure as conference/)
        ├── target.yaml
        ├── outline.md
        ├── sections/
        ├── figures/
        ├── references.bib
        ├── main.tex
        ├── review.md
        ├── revision-plan.md
        └── submission/
```

Notes:

- `paper/journal/` is optional. Only created when needed.
- `paper/conference/` is optional if the first target is journal-only.
- `.paperwriter/` stores reusable system assets, not manuscript content.
- `paper/` stores all manuscript state and is gitignored by default (user opts in
  to version control).

## State Model

### Global state: `paper/state.yaml`

```yaml
active_target: conference
initialized: true
targets:
  conference:
    stage: drafting        # init | literature | outlining | drafting | review | camera-ready | done
    created: 2027-01-15
  journal:
    stage: init
    created: 2027-03-01
```

The `stage` field per target lets agents know what has been completed and what is
expected next. Commands use this to enforce prerequisites (e.g., `/draft-paper`
requires `stage >= outlining`).

### Shared context: `paper/shared/context.md`

This is the central bridge between the research repo and the paper agents. It
contains:

```markdown
# Paper Context

## Title
[Working title]

## Topic
[2-3 sentence description of the research]

## Contributions
1. [Contribution 1]
2. [Contribution 2]
3. [Contribution 3]

## Paper Type
[Methodology | Theory | Empirical | Theory+Experiments]

## Source Map

The following paths in this repository contain materials relevant to the paper.
Agents should read from these locations when they need project context.

- Documentation: `docs/model.md`, `docs/theory.md`, `docs/experiments.md`
- Source code: `src/myproject/`
- Experiment results: `results/`
- Figures: `figures/`
- Data: `data/raw/`, `data/processed/`
- Scripts: `scripts/train.py`, `scripts/evaluate.py`

## Key Files
[Optional: annotated list of the most important files agents should read]

- `docs/model.md` — mathematical formulation of the model
- `results/main_results.csv` — primary experimental results
- `docs/theory.md` — proofs and theoretical analysis
```

### Target metadata: `paper/<target>/target.yaml`

```yaml
name: conference
venue: NeurIPS 2027
template: neurips
mode: blind             # blind | camera-ready | submission
page_limit: 8
audience: ml            # ml | econometrics | marketing | management-science | operations
```

## Command Model

### Required commands

- `/new-paper`
  - Scans repo structure (not hardcoded paths — actually walks the directory tree)
  - Asks user for title, topic, contributions, venue, paper type
  - Writes `paper/shared/context.md` with the source map
  - Creates the first target directory with `target.yaml`
  - Sets `paper/state.yaml`

- `/set-target [conference|journal]`
  - Switches the active target
  - Updates `paper/state.yaml`

- `/literature-search`
  - Reads topic from `paper/shared/context.md`
  - Spawns parallel `literature-reviewer` agents
  - Writes to `paper/shared/literature/`
  - Appends to `paper/shared/references-master.bib`
  - Advances target stage to `literature`

- `/draft-paper`
  - Reads active target from `paper/state.yaml`
  - Prerequisite: outline exists for active target
  - Spawns parallel section writers (intro, technical, empirics)
  - Runs citation-manager, then latex-assembler
  - Writes to `paper/<active_target>/sections/` and `paper/<active_target>/main.tex`
  - Advances target stage to `drafting`

- `/camera-ready`
  - Formats only the active target
  - Runs final citation check, venue-formatter, compilation
  - Writes to `paper/<active_target>/camera-ready/`
  - Advances target stage to `camera-ready`

### Additional commands

- `/create-journal-version`
  - Bootstraps `paper/journal/` from `paper/shared/`
  - Optionally uses conference outline as input, but writes fresh journal sections
  - Adds `journal` entry to `paper/state.yaml`

- `/review-paper`
  - Runs peer-reviewer on the active target
  - Writes `paper/<active_target>/review.md` and `paper/<active_target>/revision-plan.md`

## Agent Input and Output Contract

All agents first resolve the active target from `paper/state.yaml`.

Then:

- shared inputs come from `paper/shared/` plus paths listed in the source map
- target-specific inputs come from `paper/<active_target>/`
- target-specific outputs go only to `paper/<active_target>/`

### Source map resolution

When an agent needs project context (experiment results, model docs, etc.), it
reads the source map from `paper/shared/context.md` and follows the paths listed
there. Agents must NOT hardcode paths like `docs/model.md` or `results/`. If the
source map does not list a relevant path, the agent should note the gap and
proceed with available information.

### Shared paper materials agents may read

- `paper/shared/context.md`
- `paper/shared/claims.md`
- `paper/shared/literature/`
- `paper/shared/references-master.bib`
- `paper/shared/figure-plan.md`
- `paper/shared/table-plan.md`
- `paper/shared/evidence/`

### Target-specific materials agents may read and write

- `paper/<target>/target.yaml`
- `paper/<target>/outline.md`
- `paper/<target>/sections/`
- `paper/<target>/figures/`
- `paper/<target>/references.bib`
- `paper/<target>/main.tex`
- `paper/<target>/review.md`
- `paper/<target>/revision-plan.md`

## Refactor Phases

## Phase 1: Clean slate — remove legacy structure

### Objective

Remove all project-specific state and legacy architecture from the repo so it
becomes a clean scaffold.

### Tasks

- Delete `projects/` (done)
- Delete `papers/` and all paper-specific content
- Delete `literature/` (will be recreated per-project under `paper/shared/`)
- Remove any hardcoded active-paper references

### Exit criteria

- Repo contains only framework assets (agents, commands, templates, config, docs).
- Zero project-specific state.

## Phase 2: Define and document the new contract

### Objective

Rewrite all user-facing documentation around the project-local model.

### Tasks

- Rewrite `CLAUDE.md`:
  - Remove `projects/` and `papers/` assumptions
  - Remove hardcoded active-paper tables
  - Document `paper/shared/`, `paper/<target>/`, source map concept
  - Document target switching and pipeline stages
  - Keep writing style guidelines and venue requirements (these are universal)
- Rewrite `README.md`:
  - Installation instructions
  - Quick start: install → `/new-paper` → `/literature-search` → `/draft-paper` → `/camera-ready`
  - Architecture overview
  - Venue support matrix

### Exit criteria

- A new user can understand and use the system from the README alone.

## Phase 3: Update all prompts to the new path model

### Objective

Update every command and agent to use the new filesystem contract.

### Sub-phase 3a: Commands first

Update the 4 entry-point commands. These define the contract that agents must
follow.

- `.claude/commands/new-paper.md` — scan repo, write source map, create target
- `.claude/commands/literature-search.md` — write to `paper/shared/literature/`
- `.claude/commands/draft-paper.md` — read state, write to `paper/<target>/`
- `.claude/commands/camera-ready.md` — format active target

### Sub-phase 3b: Agents

Update all 9 agents to read the source map and use the new paths.

- `.claude/agents/literature-reviewer.md`
- `.claude/agents/paper-outliner.md`
- `.claude/agents/intro-writer.md`
- `.claude/agents/technical-writer.md`
- `.claude/agents/empirics-writer.md`
- `.claude/agents/citation-manager.md`
- `.claude/agents/latex-assembler.md`
- `.claude/agents/venue-formatter.md`
- `.claude/agents/peer-reviewer.md`

### Specific contract changes

- Replace all `projects/<slug>/...` with source map paths
- Replace all `papers/<slug>/...` with `paper/<target>/...`
- Replace `workspace/` references with `paper/<target>/...`
- Replace `literature/` with `paper/shared/literature/`
- Replace `current-paper.md` with `paper/state.yaml` + `paper/shared/context.md` +
  `paper/<target>/target.yaml`

### Path lint (run immediately after each file is updated)

After updating each prompt file, grep it for banned patterns:

- `projects/`
- `papers/`
- `workspace/`
- `current-paper.md`
- `literature/references` (should be `paper/shared/references-master.bib`)

Fail the phase if any banned pattern remains.

### Exit criteria

- No command or agent prompt references any legacy path.
- Path lint passes on all prompt files.

## Phase 4: Make templates target-aware

### Objective

Align LaTeX templates with the new layout.

### Tasks

- Move `templates/` to `.paperwriter/templates/`
- Ensure templates reference `paper/<target>/sections/` for `\input{}` paths
- Normalize expected section filenames across all venues:
  - `abstract.tex`, `introduction.tex`, `related_work.tex`, `methodology.tex`,
    `experiments.tex` (or `empirics.tex`), `conclusion.tex`, `appendix.tex`
- Add a `template-manifest.yaml` in each template directory listing:
  - required section files
  - optional section files
  - style file dependencies (that users must download)

### Key rule

Target prose is stored in the target directory. Templates must not assume shared
section files.

### Exit criteria

- Templates render correctly from `paper/<target>/sections/`.
- Each template has a manifest documenting its requirements.

## Phase 5: Add installation flow

### Objective

Provide a concrete, copy-based installer.

### Install script: `.paperwriter/scripts/install.sh`

```bash
#!/usr/bin/env bash
# Usage: /path/to/paper-writer/.paperwriter/scripts/install.sh [target-repo]
#
# Copies the paper-writing scaffold into the target repo.
# Safe to re-run: updates framework files, does not touch paper/ runtime state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_ROOT="${1:-.}"

# Copy framework assets
cp -R "$SOURCE_ROOT/.claude" "$TARGET_ROOT/.claude"
cp -R "$SOURCE_ROOT/.paperwriter" "$TARGET_ROOT/.paperwriter"
cp "$SOURCE_ROOT/CLAUDE.md" "$TARGET_ROOT/CLAUDE.md"

# Add paper/ to .gitignore if not already there
if ! grep -q '^paper/' "$TARGET_ROOT/.gitignore" 2>/dev/null; then
  echo 'paper/' >> "$TARGET_ROOT/.gitignore"
fi

echo "Paper-writing scaffold installed into $TARGET_ROOT"
echo "Run /new-paper in Claude Code to initialize your paper workspace."
```

### Requirements

- Installation copies only framework files, never runtime state
- Re-running the installer updates framework files without touching `paper/`
- No symlinks
- Works on macOS and Linux

### Exit criteria

- Installer can be run on a fresh repo and `/new-paper` works afterward.

## Phase 6: Add validation

### Objective

Catch regressions early.

### Validation script: `.paperwriter/scripts/validate.sh`

Checks:

1. **Path lint**: No prompt file references banned legacy paths
2. **Template lint**: Every template directory has a manifest
3. **State lint** (if `paper/` exists):
   - `paper/state.yaml` exists and is valid YAML
   - Active target directory exists
   - Active target has `target.yaml`
4. **Section lint** (if sections exist):
   - No unresolved `\ref{??}` or `\cite{??}`
   - No `TODO` markers in camera-ready stage

### Exit criteria

- `validate.sh` passes on a clean scaffold install.
- `validate.sh` catches at least one known regression pattern.

## Concrete File-by-File Change List

### Must change

- `README.md` — rewrite for install-based workflow
- `CLAUDE.md` — rewrite for project-local contract
- `.claude/commands/new-paper.md` — scan repo, write source map
- `.claude/commands/literature-search.md` — `paper/shared/literature/`
- `.claude/commands/draft-paper.md` — target-aware drafting
- `.claude/commands/camera-ready.md` — target-aware formatting
- `.claude/agents/*.md` — all 9 agents updated to new paths
- `.claude/settings.json` — review permissions

### Must add

- `.paperwriter/config.yaml` — venue registry and defaults
- `.paperwriter/templates/` — moved from `templates/`
- `.paperwriter/scripts/install.sh`
- `.paperwriter/scripts/validate.sh`

### Must remove

- `projects/` — done
- `papers/` — all project-specific paper content
- `literature/` — will be recreated per-project under `paper/shared/`
- `templates/` — moved to `.paperwriter/templates/`

## Acceptance Criteria

The implementation is complete when:

1. The repo contains zero project-specific state.
2. `install.sh` copies the scaffold into a fresh repo without errors.
3. `/new-paper` scans the target repo and produces a valid source map.
4. `/literature-search` writes to `paper/shared/literature/`.
5. `/draft-paper` writes sections to `paper/<target>/sections/` and assembles
   `main.tex`.
6. `/camera-ready` produces a submission package in
   `paper/<target>/camera-ready/`.
7. All agents read project context from the source map, not hardcoded paths.
8. Conference and journal targets are fully isolated from each other.
9. `validate.sh` passes on both a clean scaffold and an initialized project.

## Execution Order

1. Clean slate: remove legacy structure.
2. Rewrite docs (`CLAUDE.md`, `README.md`).
3. Update commands (3a), then agents (3b), with path lint after each file.
4. Move and normalize templates.
5. Write installer script.
6. Write validation script.

## Risks and Mitigations

### Risk: agents can't find project materials in unfamiliar repos

Mitigation: the source map in `paper/shared/context.md` is written during
`/new-paper` by actually scanning the repo. If `/new-paper` does its job, every
downstream agent has correct paths. If a path is missing from the source map, agents
note the gap rather than guessing.

### Risk: prompt drift during refactor

Mitigation: path lint runs after every prompt file change. Banned patterns
(`projects/`, `papers/`, `workspace/`, `current-paper.md`) are checked
automatically.

### Risk: over-sharing text between conference and journal versions

Mitigation: share evidence and plans, not section prose. Each target has its own
`sections/` directory.

### Risk: installer becomes too clever

Mitigation: the installer is a plain `cp -R` script. No package managers, no
dependency resolution, no version negotiation. Users can read and modify every file
it copies.

### Risk: source map goes stale as repo evolves

Mitigation: `/sync-evidence` command re-scans the repo and updates the source map.
Agents should also flag when a source map path doesn't exist.

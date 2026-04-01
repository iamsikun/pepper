# Academic Paper Writing System

An installable Claude Code subagent system for writing camera-ready academic papers in
**machine learning**, **marketing**, **economics**, and **operations research**.

Supports ML conferences and economics/marketing/operations journals.

---

## Installation

Pepper is a CLI tool, not a library. Install it once and use it across all your research repos.

```bash
# Install as a global CLI tool (one-time)
uv tool install git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.1.0

# Or, for local development (editable — changes take effect immediately):
uv tool install -e /path/to/pepper
```

Then in any research repo:

```bash
pepper install
```

Upgrade later:

```bash
# Upgrade to latest
uv tool upgrade pepper

# Or reinstall a specific tag:
uv tool install git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.2.0 --force

# Then sync each project:
pepper sync
```

---

## Quick Start

### Writing from scratch

```bash
# Open Claude Code in your project repo
claude

# 1. Initialize paper workspace (scans your repo, builds source map)
/new-paper

# 2. Run literature search
/literature-search

# 3. Draft the full paper
/draft-paper

# 4. Get peer review feedback
/review-paper

# 5. Revise based on feedback (iterative)
/revise-paper

# 6. Produce camera-ready submission
/camera-ready
```

### Importing an existing paper

```bash
claude

# 1. Import your existing .tex/.bib files into the pipeline
/import-paper

# 2. Choose an import mode:
#    - Review:   get feedback on your draft      → /review-paper
#    - Revise:   restructure/rewrite sections     → edit outline, then /draft-paper
#    - Retarget: adapt for a different venue       → /create-journal-version
```

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATION LAYER                        │
│  /new-paper → /literature-search → /draft-paper → /camera-ready   │
│  /import-paper ──────────────────↗ /revise-paper, /update-results │
└──────────────────────────────────────────────────────────────────┘
         │               │                │              │
         ▼               ▼                ▼              ▼
  ┌──────────┐   ┌──────────────┐  ┌──────────┐  ┌──────────┐
  │literature│   │paper-outliner│  │  intro-  │  │  venue-  │
  │-reviewer │   │              │  │  writer  │  │formatter │
  └──────────┘   └──────────────┘  └──────────┘  └──────────┘
                                   ┌──────────┐  ┌──────────┐
                                   │technical-│  │  latex-  │
                                   │  writer  │  │assembler │
                                   └──────────┘  └──────────┘
                                   ┌──────────┐  ┌──────────┐
                                   │empirics- │  │   peer-  │
                                   │  writer  │  │reviewer  │
                                   └──────────┘  └──────────┘
                                   ┌──────────┐
                                   │ citation-│
                                   │ manager  │
                                   └──────────┘
                                   ┌──────────┐
                                   │revision- │
                                   │ planner  │
                                   └──────────┘
```

---

## Agents

| Agent | Writes | When to Use |
|---|---|---|
| `literature-reviewer` | `paper/shared/literature/*.md`, BibTeX | Finding related work |
| `paper-outliner` | `paper/<target>/outline.md` | Structuring the paper |
| `intro-writer` | `abstract.tex`, `introduction.tex` | After outline is done |
| `technical-writer` | `related_work.tex`, `methodology.tex`, `appendix_proofs.tex` | Core technical content |
| `empirics-writer` | `experiments.tex` / `empirics.tex` | Results and experiments |
| `citation-manager` | `paper/<target>/references.bib` | Before assembly |
| `latex-assembler` | `paper/<target>/main.tex` | Final assembly |
| `venue-formatter` | `paper/<target>/camera-ready/` | Submission formatting |
| `peer-reviewer` | `paper/<target>/review.md`, `revision-plan.md` | Quality check |
| `revision-planner` | `paper/<target>/revisions/round-N/revision-plan.md` | Planning revisions from feedback or results changes |

---

## Commands

| Command | Purpose |
|---|---|
| `/new-paper` | Scan repo, build source map, initialize paper workspace |
| `/import-paper` | Import an existing `.tex`/`.bib` paper into the pipeline |
| `/literature-search` | Run literature search + invoke outliner |
| `/draft-paper` | Draft all sections in parallel + assemble |
| `/review-paper` | Run peer reviewer on active target |
| `/revise-paper` | Revise paper based on review feedback |
| `/update-results` | Update paper after results/data change |
| `/camera-ready` | Final formatting + submission package |
| `/set-target` | Switch active target (conference/journal) |
| `/create-journal-version` | Bootstrap journal version from shared materials |

---

## Supported Venues

Venue definitions live in `.pepper/config.yaml`. Each venue has a LaTeX template in `.pepper/templates/<venue>/`.

> **Note:** Download official `.sty`/`.cls` files from each venue's website and place them in `.pepper/templates/<venue>/`. These files cannot be distributed due to copyright.

---

## File Structure

### Scaffold files (installed into your project)

```
your-project/
├── .claude/
│   ├── agents/                  ← 10 specialized subagent prompts
│   ├── commands/                ← slash command prompts
│   └── settings.json            ← tool permissions
├── .pepper/
│   ├── config.yaml              ← system defaults (venue registry, stages)
│   ├── templates/               ← venue-specific LaTeX templates (one dir per venue)
│   └── scripts/
│       ├── install.sh           ← installer script
│       └── validate.sh          ← validation script
└── CLAUDE.md                    ← system instructions for Claude Code
```

### Runtime files (created by `/new-paper` or `/import-paper`)

```
your-project/
└── paper/
    ├── state.yaml               ← active target + per-target stages
    ├── shared/
    │   ├── context.md           ← title, topic, contributions, source map
    │   ├── claims.md            ← research claims and evidence links
    │   ├── literature/          ← survey markdown files
    │   ├── references-master.bib
    │   ├── figure-plan.md
    │   ├── table-plan.md
    │   └── evidence/
    ├── conference/              ← conference target
    │   ├── target.yaml
    │   ├── outline.md
    │   ├── sections/
    │   ├── figures/
    │   ├── references.bib
    │   ├── main.tex
    │   ├── revisions/          ← revision history
    │   │   └── round-N/
    │   │       ├── review-input.md
    │   │       ├── revision-plan.md
    │   │       ├── changelog.md
    │   │       └── sections-before/
    │   └── camera-ready/
    └── journal/                 ← (optional) journal target
        └── [same structure]
```

---

## Workflow

### Phase 1: Setup
`/new-paper` scans your repo, discovers project materials, and writes a source map so all agents know where to find things.

**Alternative:** `/import-paper` ingests an existing LaTeX paper into the `paper/` structure. It decomposes sections, copies bibliography and figures, and enters the pipeline mid-stream (at `drafting` for review/retarget, or `outlining` for restructuring).

### Phase 2: Research
`/literature-search` spawns parallel literature-reviewer agents, consolidates bibliography, then invokes paper-outliner.

### Phase 3: Drafting (parallel)
`/draft-paper` spawns intro-writer, technical-writer, and empirics-writer in parallel. Then runs citation-manager and latex-assembler sequentially.

### Phase 4: Quality Check
`/review-paper` runs the peer-reviewer agent and produces a review + revision plan.

### Phase 5: Revision (iterative)
`/revise-paper` takes review feedback, generates a structured revision plan via the revision-planner agent, selectively re-invokes writer agents, and re-assembles the paper. Each round is preserved in `paper/<target>/revisions/round-N/`.

`/update-results` is a lighter variant for when experimental results or data change — same flow but focused on propagating content changes rather than addressing reviewer criticism.

Both commands support multiple rounds and can be repeated as needed.

### Phase 6: Camera-Ready
`/camera-ready` runs final citation check, venue formatting, compilation, and produces a submission package.

---

## Multi-Target Support

One project can have up to two publication targets: conference and journal. They share research materials (`paper/shared/`) but maintain separate prose and builds.

- `/create-journal-version` — bootstrap a journal version
- `/set-target` — switch active target

---

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) for installing pepper as a CLI tool
- Claude Code installed and running
- LaTeX distribution (TeX Live or MiKTeX) for compilation
- Venue style files downloaded (see `.pepper/templates/` for which files are needed)

---

## Version

System v3.0 — Global CLI tool, project-local scaffold.

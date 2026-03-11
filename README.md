# Academic Paper Writing System

An installable Claude Code subagent system for writing camera-ready academic papers in
**machine learning**, **marketing**, **economics**, and **operations research**.

Targets: NeurIPS · ICML · ICLR · Econometrica · Marketing Science · Management Science

---

## Installation

```bash
# Add the private package to a project repo
uv add --dev git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.1.0

# Materialize the scaffold into that repo
uv run pepper install
```

Upgrade later:

```bash
uv add --dev git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.2.0
uv run pepper sync
```

---

## Quick Start

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

# 5. Produce camera-ready submission
/camera-ready
```

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATION LAYER                        │
│  /new-paper → /literature-search → /draft-paper → /camera-ready  │
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

---

## Commands

| Command | Purpose |
|---|---|
| `/new-paper` | Scan repo, build source map, initialize paper workspace |
| `/literature-search` | Run literature search + invoke outliner |
| `/draft-paper` | Draft all sections in parallel + assemble |
| `/review-paper` | Run peer reviewer on active target |
| `/camera-ready` | Final formatting + submission package |
| `/set-target` | Switch active target (conference/journal) |
| `/create-journal-version` | Bootstrap journal version from shared materials |

---

## Supported Venues

### ML Conferences
| Venue | Style | Pages | Blind |
|---|---|---|---|
| NeurIPS | `neurips_2025.sty` | 8+refs | Yes |
| ICML | `icml2025.sty` | 8+refs | Yes |
| ICLR | `iclr2025.sty` | 9+refs | Yes |

### Journals
| Venue | Style | Blind |
|---|---|---|
| Econometrica | `ecta.cls` | Yes |
| Marketing Science | `informs4.cls` | Yes |
| Management Science | `informs4.cls` | Yes |

> **Note:** Download official `.sty`/`.cls` files from each venue's website and place them in `.pepper/templates/<venue>/`. These files cannot be distributed due to copyright.

---

## File Structure

### Scaffold files (installed into your project)

```
your-project/
├── .claude/
│   ├── agents/                  ← 9 specialized subagent prompts
│   ├── commands/                ← slash command prompts
│   └── settings.json            ← tool permissions
├── .pepper/
│   ├── config.yaml              ← system defaults (venue registry, stages)
│   ├── templates/               ← venue-specific LaTeX templates
│   │   ├── neurips/
│   │   ├── icml/
│   │   ├── iclr/
│   │   ├── econometrica/
│   │   └── informs/
│   └── scripts/
│       ├── install.sh           ← installer script
│       └── validate.sh          ← validation script
└── CLAUDE.md                    ← system instructions for Claude Code
```

### Runtime files (created by `/new-paper`)

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
    │   └── camera-ready/
    └── journal/                 ← (optional) journal target
        └── [same structure]
```

---

## Workflow

### Phase 1: Setup
`/new-paper` scans your repo, discovers project materials, and writes a source map so all agents know where to find things.

### Phase 2: Research
`/literature-search` spawns parallel literature-reviewer agents, consolidates bibliography, then invokes paper-outliner.

### Phase 3: Drafting (parallel)
`/draft-paper` spawns intro-writer, technical-writer, and empirics-writer in parallel. Then runs citation-manager and latex-assembler sequentially.

### Phase 4: Quality Check
`/review-paper` runs the peer-reviewer agent and produces a review + revision plan.

### Phase 5: Camera-Ready
`/camera-ready` runs final citation check, venue formatting, compilation, and produces a submission package.

---

## Multi-Target Support

One project can have up to two publication targets: conference and journal. They share research materials (`paper/shared/`) but maintain separate prose and builds.

- `/create-journal-version` — bootstrap a journal version
- `/set-target` — switch active target

---

## Prerequisites

- Claude Code installed and running
- LaTeX distribution (TeX Live or MiKTeX) for compilation
- Venue style files downloaded (see `.pepper/templates/` for which files are needed)

---

## Version

System v3.0 — Project-local `uv`-managed package scaffold.

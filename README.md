# Academic Paper Writing System

A Claude Code subagent system for writing camera-ready academic papers in
**machine learning**, **marketing**, and **operations research**.

Targets: NeurIPS · ICML · ICLR · Econometrica · Marketing Science · Management Science

---

## Quick Start

```bash
# 1. Clone / copy this system into your project directory
# 2. Open Claude Code in this directory
claude

# 3. Initialize a new paper
/new-paper

# 4. Run literature search
/literature-search

# 5. Draft the full paper
/draft-paper

# 6. Get peer review feedback
# Invoke peer-reviewer agent: "Use the peer-reviewer agent on my paper"

# 7. Produce camera-ready submission
/camera-ready
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION LAYER                      │
│  /new-paper → /literature-search → /draft-paper → /camera-ready │
└─────────────────────────────────────────────────────────────┘
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
| `literature-reviewer` | `research/literature/*.md`, BibTeX | Finding related work |
| `paper-outliner` | `workspace/paper-outline.md` | Structuring the paper |
| `intro-writer` | `abstract.tex`, `introduction.tex` | After outline is done |
| `technical-writer` | `related_work.tex`, `methodology.tex`, `appendix_proofs.tex` | Core technical content |
| `empirics-writer` | `experiments.tex` / `empirics.tex` | Results and experiments |
| `citation-manager` | `references.bib` | Before assembly |
| `latex-assembler` | `papers/<slug>/main.tex` | Final assembly |
| `venue-formatter` | `camera-ready/` folder | Submission formatting |
| `peer-reviewer` | `review.md`, `revision-plan.md` | Quality check |

---

## Commands

| Command | Purpose |
|---|---|
| `/new-paper` | Initialize a new paper project |
| `/literature-search` | Run literature search + invoke outliner |
| `/draft-paper` | Draft all sections in parallel + assemble |
| `/camera-ready` | Final formatting + submission package |

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

> **Note:** You must download the official `.sty` / `.cls` files from each venue's website
> and place them in the appropriate `templates/<venue>/` folder. These files cannot be
> distributed with this system due to copyright.

---

## File Structure

```
academic-paper-system/
├── CLAUDE.md                    ← Main system context (read by Claude Code)
├── README.md                    ← This file
├── .claude/
│   ├── agents/                  ← 9 specialized subagents
│   │   ├── literature-reviewer.md
│   │   ├── paper-outliner.md
│   │   ├── intro-writer.md
│   │   ├── technical-writer.md
│   │   ├── empirics-writer.md
│   │   ├── citation-manager.md
│   │   ├── latex-assembler.md
│   │   ├── venue-formatter.md
│   │   └── peer-reviewer.md
│   ├── commands/                ← 4 slash commands
│   │   ├── new-paper.md
│   │   ├── literature-search.md
│   │   ├── draft-paper.md
│   │   └── camera-ready.md
│   └── settings.json
├── templates/                   ← LaTeX templates per venue
│   ├── neurips/main.tex
│   ├── icml/main.tex
│   ├── iclr/main.tex
│   ├── informs/main.tex         ← Marketing Science & Management Science
│   └── econometrica/main.tex
├── workspace/                   ← Active paper workspace (auto-created)
│   ├── current-paper.md         ← Pipeline state tracker
│   ├── paper-outline.md
│   └── sections/                ← Individual .tex section files
├── research/
│   └── literature/              ← Literature review outputs + master BibTeX
└── papers/                      ← Assembled papers
    └── <paper-slug>/
        ├── main.tex
        ├── references.bib
        ├── figures/
        └── camera-ready/        ← Final submission package
```

---

## Workflow Detail

### Phase 1: Setup
```
/new-paper  →  Creates workspace/current-paper.md
            →  Copies venue template
            →  Initializes directory structure
```

### Phase 2: Research
```
/literature-search  →  [parallel] literature-reviewer × 2-3 threads
                    →  Consolidated references.bib
                    →  paper-outliner creates paper-outline.md
```

### Phase 3: Drafting (parallel)
```
/draft-paper  →  [parallel] intro-writer
              →  [parallel] technical-writer  (related work + method + proofs)
              →  [parallel] empirics-writer   (experiments/empirics)
              →  [sequential] citation-manager
              →  [sequential] latex-assembler
```

### Phase 4: Quality Check
```
peer-reviewer  →  review.md  (scores, weaknesses, required changes)
               →  revision-plan.md
```

### Phase 5: Camera-Ready
```
/camera-ready  →  citation-manager (final pass)
               →  venue-formatter  (style, page count, checklist)
               →  Compilation check
               →  papers/<slug>/submission.zip
```

---

## Tips

- **Invoke agents explicitly** when you want specific control:
  `"Use the technical-writer agent to write the methodology section for a Bayesian optimization paper"`

- **For revisions**, invoke the relevant agent directly:
  `"Use the empirics-writer agent to add a robustness check using [X]"`

- **Token efficiency**: Each agent has its own context window, so parallel search
  won't exhaust your main context.

- **Real results**: Agents write placeholder text around `% TODO:` markers for
  actual figures and numbers. Fill these in after running your real experiments.

---

## Prerequisites

- Claude Code installed and running
- LaTeX distribution (TeX Live or MiKTeX) for compilation
- Venue style files downloaded (see templates/ for which files are needed)

---

## Version

System v1.0 — Designed for 2025 submission cycles.
Update venue style files each year as venues release new templates.

# Academic Paper Writing System

## Researcher Profile

**Domains:** Machine Learning, Marketing, Econometrics, Operations, Quant Finance
**Target Venues:**
- ML Conferences: NeurIPS, ICML, ICLR, AAAI
- Journals: Econometrica, Marketing Science, Management Science, Journal of Marketing Research, Operations Research

---

## System Architecture

This system uses a pipeline of specialized subagents to produce camera-ready academic papers. The pipeline is:

```
[/new-paper] → literature-reviewer → paper-outliner
                                         ↓
                         ┌───────────────┼───────────────┐
                    intro-writer   technical-writer  empirics-writer
                         └───────────────┼───────────────┘
                                         ↓
                              citation-manager
                                         ↓
                              latex-assembler
                                         ↓
                              venue-formatter
                                         ↓
                              peer-reviewer
                                    ↓    ↑
                            revision-planner ←─ /revise-paper, /update-results
                                    ↓
                         selective writer re-invocation
                                    ↓
                           [camera-ready output]
```

Pipeline state is tracked in `paper/state.yaml`. Each target (conference/journal) has its own stage.

---

## Target Resolution Protocol

All agents and commands resolve their context through these files:

1. **`paper/state.yaml`** → `active_target` (conference or journal) + per-target stage
2. **`paper/shared/context.md`** → title, topic, contributions, paper type, **source map**
3. **`paper/<active_target>/target.yaml`** → venue, template, mode, page_limit, audience
4. **Source map paths** → project-specific locations for docs, code, results, data

Agents must NOT hardcode paths like `docs/model.md` or `results/`. If a source map path is missing, note the gap and proceed with available information.

---

## Paper Management

All paper state lives in `paper/` at the repository root:

```
paper/
├── state.yaml                    ← global state: active target, per-target stages
├── shared/
│   ├── context.md               ← title, topic, contributions, source map
│   ├── claims.md                ← research claims and evidence links
│   ├── literature/              ← survey markdown files per topic
│   ├── references-master.bib    ← master BibTeX file
│   ├── figure-plan.md           ← planned figures with descriptions
│   ├── table-plan.md            ← planned tables with descriptions
│   └── evidence/                ← verified results, numbers, quotes
├── conference/                   ← conference target
│   ├── target.yaml              ← venue, template, mode, page limit, audience
│   ├── outline.md               ← section-level outline
│   ├── sections/                ← .tex drafts
│   ├── figures/                 ← target-specific figures
│   ├── references.bib           ← subset of master bib
│   ├── main.tex                 ← assembled paper
│   ├── review.md                ← peer review output
│   ├── revision-plan.md         ← actionable revision steps
│   ├── revisions/               ← revision history
│   │   └── round-N/
│   │       ├── review-input.md
│   │       ├── revision-plan.md
│   │       ├── changelog.md
│   │       └── sections-before/
│   └── camera-ready/            ← submission package
└── journal/                      ← (optional, same structure as conference/)
    ├── target.yaml
    ├── outline.md
    ├── sections/
    ├── figures/
    ├── references.bib
    ├── main.tex
    ├── review.md
    ├── revision-plan.md
    ├── revisions/
    │   └── round-N/
    │       ├── review-input.md
    │       ├── revision-plan.md
    │       ├── changelog.md
    │       └── sections-before/
    └── submission/
```

### Shared vs Target-Specific

**Shared** (`paper/shared/`): problem framing, claims, evidence, literature, bibliography, figure/table plans. These are the research truth — shared across targets.

**Target-specific** (`paper/<target>/`): section prose, outline, assembled paper, review feedback. Never share raw section text between targets.

---

## Project Context

This system is project-local. The repository IS the project. There is no `projects/` indirection.

When `/new-paper` runs, it scans the repo tree and writes a **source map** into `paper/shared/context.md` that tells all downstream agents where to find project materials:

```markdown
## Source Map
- Documentation: `docs/model.md`, `docs/theory.md`
- Source code: `src/myproject/`
- Experiment results: `results/`
- Figures: `figures/`
- Data: `data/raw/`, `data/processed/`
```

Agents read the source map rather than guessing paths.

---

## Templates

LaTeX templates live in `.pepper/templates/<venue>/main.tex`. Each venue directory also contains a `template-manifest.yaml` describing required style files, sections, and formatting rules.

Users must download official `.sty`/`.cls` files from venue websites and place them in the appropriate template directory.

---

## Writing Style Guidelines

### Universal Rules
- Every claim needs either a citation or a proof
- Define all notation and abbreviation before using it
- Tables and figures need to be self-contained: readers can understand the message at first glance
- Figures: always include captions that are self-contained
- Never use "we show" without actually showing it

### For ML Papers (NeurIPS / ICML / ICLR)
- Lead with a clear **problem statement** and **why it matters**
- State contributions as a bulleted list in the introduction (3-5 bullet points)
- Methodology: formal definitions first, then algorithm, then theoretical guarantees
- Use `\theorem`, `\lemma`, `\proof` environments for all theoretical claims
- Experiments: ablation studies are mandatory; always report mean +/- std over multiple seeds
- Related work: position clearly against at least 10 recent papers
- 8 pages main body + unlimited references

### For Economics/Marketing/Operations Papers (Econometrica, Management Science, Marketing Science)
- Abstract should state: research question, method, finding, contribution — in that order
- Introduction
  - Must state why the problem matters for actual businesses
  - Must include a "Contribution" paragraph
- (Stylized) Modeling papers: model setup → equilibrium analysis → comparative statics
- Theory papers: data generation process → model → theory (convergence etc.) → experiments
- Empirical papers: data → identification strategy → results → robustness
- Formal propositions with proofs
  - Intuition for the proof (i.e., why the proposition/theorem holds) in the main body
  - Full proofs in appendix
- Style is more formal and discursive than ML papers

---

## Venue-Specific Requirements

| Venue | Format | Page Limit | Style File |
|---|---|---|---|
| NeurIPS | Double-column | 8+refs | `neurips_2025.sty` |
| ICML | Double-column | 8+refs | `icml2025.sty` |
| ICLR | Single-column | 9+refs | `iclr2025.sty` |
| Econometrica | Single-column | No limit | `ecta.cls` |
| Marketing Science | Single-column | 40 pages | INFORMS |
| Management Science | Single-column | 40 pages | INFORMS |

---

## Pipeline Stages

Each target progresses through: `init` → `literature` → `outlining` → `drafting` → `review` → `revising` → `camera-ready` → `done`

Commands enforce prerequisites based on the current stage.

---

## Revision Workflow

The pipeline supports iterative revision through two commands:

### `/revise-paper` — Review-Driven Revision
Use after receiving peer review feedback (from `/review-paper` or actual reviewers). Flow:
1. Saves review feedback and backs up current sections
2. `revision-planner` agent maps each comment to specific section changes
3. User reviews and approves the revision plan
4. Writer agents selectively revise only affected sections
5. Paper is re-assembled and compiled

### `/update-results` — Results-Driven Update
Use when experimental results, figures, or data change (not review-driven). Same flow as
`/revise-paper` but the revision planner focuses on propagating content changes rather than
addressing reviewer criticism. Stage stays at `drafting`.

### Revision History
Each revision round is preserved in `paper/<target>/revisions/round-<N>/`:
- `review-input.md` — the original feedback or change description
- `revision-plan.md` — the structured plan produced by revision-planner
- `changelog.md` — summary of changes made
- `sections-before/` — backup of all .tex files before revision

### Writer Revision Mode
When invoked during a revision, writer agents (intro-writer, technical-writer, empirics-writer)
operate in revision mode: they read existing sections first, make only the changes specified
in the revision plan, and add `% REVISED: <note>` comments for traceability.

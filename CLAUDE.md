# Academic Paper Writing System

## Researcher Profile

**Domains:** Machine Learning, Marketing, Econometrics, Operations, Quant Finance
**Target Venues:**
- ML Conferences: NeurIPS, ICML, ICLR, AAAI
- Journals: Econometrica, Marketing Science, Management Science, Journal of Marketing Research, Operations Research

**Current Paper:** See `workspace/current-paper.md` if it exists.

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
                                         ↓
                           [camera-ready output]
```

---

## Active Workspace

When working on a paper, always check `workspace/current-paper.md` for:
- Paper title, topic, and venue
- Key contributions (explicitly stated)
- Current pipeline stage
- File locations for each section

Sections are saved to `workspace/sections/` as `.tex` files.  
Literature notes are in `research/literature/`.  
The assembled paper is in `papers/<paper-slug>/`.

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
- State contributions as a bulleted list in the introduction (3–5 bullet points)
- Methodology: formal definitions first, then algorithm, then theoretical guarantees
- Use `\theorem`, `\lemma`, `\proof` environments for all theoretical claims
- Experiments: ablation studies are mandatory; always report mean ± std over multiple seeds
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
  - Intuition for the proof (i.e., why the proposition/theorem holds ) in the main body
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

Templates are in `templates/<venue>/main.tex`.

---

## Paper Management

All papers live in `papers/<slug>/`. Each paper has its own workspace:

```
papers/<slug>/
├── workspace/
│   ├── current-paper.md              ← pipeline state for this paper
│   ├── paper-outline.md
│   ├── sections/                     ← .tex drafts for this paper
│       ├── abstract.tex
│       ├── introduction.tex
│       ├── related_work.tex
│       ├── methodology.tex          
│       ├── (optional) data.tex      ← good to have for empirical papers
│       ├── experiments.tex          ← or empirics.tex for econ/marketing papers
│       ├── conclusion.tex
│       └── appendix.tex
│   └── notes.md                      ← scratch notes, reviewer feedback
├── main.tex                          ← assembled paper
├── references.bib                    ← paper-specific (subset of master)
├── figures/
└── camera-ready/                     ← final submission-ready files
```

### Shared Resources (across all papers)
```
literature/
├── references-master.bib     ← master BibTeX file (all papers)
└── <topic>-survey.md         ← literature summary for each topic
```

## Projects 

Each project rougly follows the layout (agents should look here for project docs and related experiment results)
```
projects/<slug>/
├── src/<project-name>        ← source code for project
├── scripts/                  ← scripts for running the experiments
├── results/                  ← raw experiment outputs
├── docs/                     ← markdown files describing models, theories, experiments, etc.
│   ├── model.md              ← describes the data generation process, models, etc.
│   ├── theory.md             ← contains lemmas, propositions, theorems, and proofs, etc.
│   ├── simulation.md         ← describes how the simulation experiments are setup 
│   ├── experiments.md        ← describes how the experiments are setup 
│   └── analysis.md           ← scratch notes on what the results mean
└── data/                     ← raw data folder 
```

## Active Paper

| Slug | Project Path | Type | Paper Target |
|---|---|---|---|
| ask-factors | projects/ask-factors/ | ML + Quant | NeurIPS 2026 |
| recsys | projects/recsys/ | ML + Marketing | NeurIPS 2026 |

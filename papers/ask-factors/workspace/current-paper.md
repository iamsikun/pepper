# Current Paper

## Metadata
- **Title:** Interpretable and Tradable Factors from Mutual Funds via Deep Autoencoding with Alternative Data
- **Slug:** ask-factors
- **Venue:** NeurIPS 2026
- **Type:** Methodology
- **Created:** 2026-03-04

## Research Topic
We propose an Autoencoding Factor Model (AFM) that extracts latent factors from mutual fund returns using a neural autoencoder with a portfolio bottleneck. Each factor is defined as the return of an explicit, tradable portfolio whose weights are conditioned on fund characteristics (economic sector holdings, asset class allocations) and a learned market-state embedding. The model jointly learns portfolio weights, conditional factor loadings, and asset intercepts end-to-end, producing factors that are simultaneously tradable, interpretable, and predictive across 10 asset classes.

## Key Contributions
1. **Portfolio bottleneck architecture** -- A neural autoencoder where each latent factor is the return of a tradable portfolio with explicit, no-look-ahead weights, bridging deep latent factor models and traditional portfolio-based factor construction.
2. **Conditional factor structure via alternative data** -- Factor portfolio weights and loadings are conditioned on mutual fund characteristics (sector holdings, asset class allocations), enabling interpretable, time-varying factor exposures.
3. **Cross-asset factor learning** -- Multi-asset training across 10 categories (equities, bonds, REITs, EM) achieves 85.0% average OOS R-squared vs. 68.4% for Fama-French, with the largest gains on non-equity assets where traditional factors fail.
4. **Comprehensive empirical evaluation** -- Ablation studies across architectures (MLP vs. residual MLP), training universes (single-asset vs. multi-asset), and baselines demonstrate the value of the portfolio bottleneck and characteristic conditioning.

## Pipeline Status
- [x] Literature review (`/literature-search`)
- [x] Paper outline (`paper-outliner` agent) -- completed 2026-03-04
- [x] Introduction + Abstract (`intro-writer` agent)
- [x] Technical sections (`technical-writer` agent)
- [x] Experiments/Empirics (`empirics-writer` agent)
- [x] Citations (`citation-manager` agent)
- [x] Assembly (`latex-assembler` agent) -- completed 2026-03-04
- [ ] Venue formatting (`venue-formatter` agent)
- [ ] Peer review (`peer-reviewer` agent)
- [ ] Camera-ready (`/camera-ready`)

## Assembly Notes (2026-03-04)
- **Compilation status:** Successful (pdflatex + bibtex, no errors)
- **Page count:** 15 pages total (main body + references + appendix)
- **Warnings:** Minor bibtex warning on `Duan2022factorvae` (volume+number conflict); no undefined references or citations
- **Fixes applied during assembly:**
  - Fixed duplicate `\label{sec:setup}` between methodology.tex and experiments.tex (renamed to `sec:exp_setup` in experiments)
  - Added placeholder figures for `fig:architecture`, `fig:r2_comparison`, and `fig:loss_trajectories` (figure files not yet created)
  - Created minimal `neurips_2025.sty` for compilation (replace with official style file for camera-ready)
  - Section .tex files copied to `papers/ask-factors/sections/` for `\input{}` inclusion
- **Items needing human attention:**
  1. Replace `neurips_2025.sty` with the official NeurIPS 2025/2026 style file
  2. Create actual figures: `figures/architecture.pdf`, `figures/r2_comparison.pdf`, `figures/loss_trajectories.pdf`
  3. Review TODO comments in introduction.tex (lines with `% TODO: verify`)
  4. Review TODO comments in experiments.tex (GPU model, wall-clock times)
  5. Review TODO comments in appendix_experiments.tex (per-fund distributions, factor analysis, sensitivity)
  6. Current page count (15) exceeds NeurIPS 8-page main body limit; will need trimming after official style file is applied

## File Locations
- Outline: `papers/ask-factors/workspace/paper-outline.md`
- Sections: `papers/ask-factors/workspace/sections/`
- Assembled sections: `papers/ask-factors/sections/`
- Literature: `literature/`
- Assembled: `papers/ask-factors/main.tex`
- Camera-ready: `papers/ask-factors/camera-ready/`
- Connected project: `projects/ask-factors/`

## Section Drafting Instructions

### intro-writer agent
- **Read from:**
  - `papers/ask-factors/workspace/paper-outline.md` (Abstract and S1 Introduction outline)
  - `literature/deep-factor-models-survey.md` (for citations and positioning)
  - `literature/alternative-data-fund-survey.md` (for fund-level data context)
  - `projects/ask-factors/docs/analysis.md` (for headline result numbers)
- **Write to:**
  - `papers/ask-factors/workspace/sections/abstract.tex`
  - `papers/ask-factors/workspace/sections/introduction.tex`

### literature-reviewer agent (Related Work)
- **Read from:**
  - `papers/ask-factors/workspace/paper-outline.md` (S2 Related Work outline)
  - `literature/deep-factor-models-survey.md`
  - `literature/portfolio-factor-construction-survey.md`
  - `literature/alternative-data-fund-survey.md`
  - `literature/autoencoders-finance-survey.md`
- **Write to:**
  - `papers/ask-factors/workspace/sections/related_work.tex`

### technical-writer agent (Method)
- **Read from:**
  - `papers/ask-factors/workspace/paper-outline.md` (S3 Method outline)
  - `projects/ask-factors/docs/model.md` (precise mathematical notation, all equations)
  - `projects/ask-factors/docs/training_pipeline.md` (training procedure details)
- **Write to:**
  - `papers/ask-factors/workspace/sections/methodology.tex`

### empirics-writer agent (Experiments)
- **Read from:**
  - `papers/ask-factors/workspace/paper-outline.md` (S4 Experiments outline)
  - `projects/ask-factors/docs/analysis.md` (all result numbers, per-category breakdowns)
  - `projects/ask-factors/docs/context.md` (data description, model configurations)
  - `projects/ask-factors/results/analysis/r2_comparison.csv` (raw numbers for tables)
- **Write to:**
  - `papers/ask-factors/workspace/sections/experiments.tex`

### technical-writer agent (Conclusion)
- **Read from:**
  - `papers/ask-factors/workspace/paper-outline.md` (S5 Conclusion outline)
- **Write to:**
  - `papers/ask-factors/workspace/sections/conclusion.tex`
  - `papers/ask-factors/workspace/sections/appendix.tex`

## Notes
- Target: NeurIPS 2026 (8 pages + unlimited references, double-column)
- 5 factors: 2 long-only, 3 long-short market-neutral
- Best model: single-layer MLP, all assets, 85.0% avg OOS R-squared
- Experiment results in `projects/ask-factors/results/`
- Model/training details in `projects/ask-factors/docs/`

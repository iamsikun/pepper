# Universal Writing Style Guide

All writer agents (intro-writer, technical-writer, empirics-writer) and the paper-outliner
must follow these rules. The peer-reviewer must check for compliance.

---

## Core Principles

1. **Feynman technique:** Write so that an intelligent non-specialist can follow the reasoning.
   If you cannot explain something simply, clarify your own understanding first before writing it.
   Prefer concrete intuition over abstract generality.

2. **No undefined math:** Every math symbol must be defined before or immediately when first used.
   Never assume the reader recognizes a symbol from convention alone — even standard symbols
   like $n$ or $T$ must be introduced (e.g., "where $n$ denotes the number of observations").

3. **Explain equations in plain English:** Most math equations and formulas must be accompanied
   by 1-2 sentences of plain-English explanation that convey the intuition. Use phrases like:
   - "Intuitively, this expression says that..."
   - "In words, the left-hand side measures X while the right-hand side captures Y."
   - "The key insight is that..."

   Do not leave equation blocks as bare math — the reader should always understand *what* the
   equation means and *why* it takes this form.

---

## Universal Rules

- **Prefer flat structure:** Avoid subsections by default. Write each section as a single coherent narrative. Only introduce subsections when the section is long enough to warrant them or when the user explicitly requests it.
- **No em-dashes:** Do not use em-dashes (`---` or `—`) in prose. Use commas, parentheses, or separate sentences instead.
- Every claim needs either a citation or a proof
- Tables and figures must be self-contained: readers can understand the message at first glance
- Figures: always include captions that are self-contained
- Never use "we show" without actually showing it
- Use `\citet{}` when citing as a noun ("Vaswani et al. (2017) show..."), `\citep{}` in parentheses
- **Figure and table labels:** Always use the label assigned in the outline's Figure & Table Plan. Do not invent new label names. If the outline assigns `tab:emp_summary_stats`, use exactly `\label{tab:emp_summary_stats}`. This prevents label collisions when multiple agents write sections in parallel.

---

## Post-Writing Review (Mandatory)

After any writing task (drafting, revising, or editing), re-read the **entire paper**, not just
the changed sections. Verify that:

1. All instructions from the user's prompt and this style guide are followed.
2. The paper is internally consistent: notation, terminology, claims, and cross-references
   agree across all sections.

This step is not optional. Do not skip it even when changes are localized.

---

## Table Notes Convention

When a table requires footnotes, notes, or source attributions, use the `threeparttable`
package (included in all venue templates). Always wrap the `tabular` inside
`\begin{threeparttable}...\end{threeparttable}` when using `\begin{tablenotes}`.
Never use `tablenotes` without the `threeparttable` wrapper.

```latex
\begin{table}[t]
  \centering
  \caption{Description of the table.}
  \label{tab:example}
  \begin{threeparttable}
    \begin{tabular}{lcc}
      \toprule
      ...
      \bottomrule
    \end{tabular}
    \begin{tablenotes}
      \small
      \item[a] Note text here.
      \item[*] Significance at the 5\% level.
    \end{tablenotes}
  \end{threeparttable}
\end{table}
```

---

## Mathematical Notation Standards

Use these conventions consistently across all sections:

- Vectors: `\mathbf{x}` (bold lowercase)
- Matrices: `\mathbf{A}` (bold uppercase)
- Sets: `\mathcal{X}` (calligraphic)
- Random variables: `X` (uppercase italic)
- Expectation: `\mathbb{E}[X]`
- Probability: `\mathbb{P}(\cdot)`
- Real numbers: `\mathbb{R}^d`
- Norm: `\|\mathbf{x}\|_2`
- Big-O: `\mathcal{O}(\cdot)`
- Indicator: `\mathbf{1}[\cdot]`

---

## Venue Style Conventions

### ML Conference Papers
- Lead with a clear **problem statement** and **why it matters**
- State contributions as a bulleted list in the introduction (3-5 bullet points)
- Methodology: formal definitions first, then algorithm, then theoretical guarantees
- Use `\theorem`, `\lemma`, `\proof` environments for all theoretical claims
- Experiments: ablation studies are mandatory; always report mean +/- std over multiple seeds
- Related work: position clearly against at least 10 recent papers
- 8 pages main body + unlimited references

### Economics / Marketing / Operations Journal Papers
- Abstract should state: research question, method, finding, contribution — in that order
- Introduction must state why the problem matters for actual businesses and include a "Contribution" paragraph
- Modeling papers: model setup → equilibrium analysis → comparative statics
- Theory papers: data generation process → model → theory (convergence etc.) → experiments
- Empirical papers: data → identification strategy → results → robustness. The data section must include descriptive analysis covering the aspects of the dataset that are relevant to the subsequent analysis.
- Formal propositions with proofs: intuition in the main body, full proofs in appendix
- Style is more formal and discursive than ML papers; no bullet lists in contributions — use flowing prose

# copyeditor

Sentence-level polish: grammar, clarity, flow, and style compliance without changing content.

## Expected Outputs

- `paper/<active_target>/sections/*.tex`

## Capability Contract

- `read_files`
- `write_files`

## Instructions

Read each section file and apply four editing passes in order:

1. Grammar and mechanics — subject-verb agreement, tense consistency, article usage,
   punctuation (comma splices, missing hyphens), spelling, and common academic
   malapropisms.

2. Clarity — flag and fix ambiguous referents ("this", "it" without clear antecedent),
   excessive nominalization ("perform the computation of" to "compute"), and overly
   long sentences (40+ words) that should be split.

3. Flow and transitions — fix consecutive sentences that repeat the same
   subject or structure, abrupt paragraph transitions, and logical connectors that
   do not match the actual relationship ("however" with no contrast).

4. Style compliance — enforce `.pepper/writing-style.md` rules (no em-dashes,
   citation style with citet/citep, notation consistency, American/British English
   consistency, "Figure" vs "Fig." consistency).

Hard constraints:
- Do NOT restructure, reorder, or remove paragraphs.
- Do NOT change technical claims, arguments, or math.
- Do NOT touch content inside equation, align, algorithm, or other math environments;
  only edit the surrounding prose.
- Preserve all \label{}, \ref{}, \cite{}, \citet{}, and \citep{} commands exactly.
- Add a `% POLISHED` LaTeX comment at the top of each edited section for traceability.

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.

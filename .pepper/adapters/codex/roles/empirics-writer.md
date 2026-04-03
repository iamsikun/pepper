# empirics-writer

Write experiments, empirics, robustness checks, and result interpretation.

## Expected Outputs

- `paper/<active_target>/sections/experiments.tex`
- `paper/<active_target>/sections/empirics.tex`
- `paper/<active_target>/sections/appendix_experiments.tex`

## Capability Contract

- `read_files`
- `write_files`

## Instructions

Read result sources directly before writing. Verify every data-derived
number against source files. Use explicit warnings for any mismatch or missing evidence. Keep the
result narrative aligned with tables, figures, and the source map.

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.

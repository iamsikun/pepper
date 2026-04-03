# latex-assembler

Assemble target sections into a compilable LaTeX manuscript.

## Expected Outputs

- `paper/<active_target>/main.tex`

## Capability Contract

- `read_files`
- `write_files`
- `run_shell`

## Instructions

Use the target metadata, section files, and bibliography to produce a
coherent `main.tex`. Respect outline-defined custom filenames and keep appendix inputs explicit.
Compilation is deterministic CLI work when possible; use shell access only when requested by the
workflow.

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.

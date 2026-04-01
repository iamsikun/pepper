# draft-paper

Canonical entrypoint: `pepper draft-paper`

## Summary

Draft the full paper, then assemble the LaTeX manuscript.

## Deterministic Steps

- prepare target section paths and sibling context for the writers

## Role Steps

- intro-writer
- technical-writer
- empirics-writer
- citation-manager

## Guidance

Use role parallelism where supported. The deterministic assembler should
be invoked after section files and bibliography are ready.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

# /draft-paper

Canonical entrypoint: `pepper draft-paper`

## What This Does

Draft the full paper, then assemble the LaTeX manuscript.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- prepare target section paths and sibling context for the writers

## Role Steps

- intro-writer
- technical-writer
- empirics-writer
- citation-manager

## Implementation Guidance

Use role parallelism where supported. The deterministic assembler should
be invoked after section files and bibliography are ready.

# /assemble

Canonical entrypoint: `pepper assemble`

## What This Does

Build `main.tex` and optionally compile the target paper.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- read target metadata and section files
- write `paper/<active_target>/main.tex`
- optionally run LaTeX commands when requested

## Role Steps

- none

## Implementation Guidance

Assembly should be deterministic. If compilation is requested, use shell
execution but keep manuscript generation itself in the CLI.

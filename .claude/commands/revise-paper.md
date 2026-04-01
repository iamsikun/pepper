# /revise-paper

Canonical entrypoint: `pepper revise-paper`

## What This Does

Plan and apply revisions from feedback or updated results.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- determine revision mode and round number
- persist revision input and backup the current sections

## Role Steps

- revision-planner
- intro-writer
- technical-writer
- empirics-writer

## Implementation Guidance

Use the planner to map work first. After user confirmation, invoke only
the required writers, then run deterministic assembly and bookkeeping.

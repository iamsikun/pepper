# /draft-section

Canonical entrypoint: `pepper draft-section`

## What This Does

Draft or revise specific sections with optional custom guidance.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- resolve the requested section names, filenames, and write/revise mode

## Role Steps

- intro-writer
- technical-writer
- empirics-writer

## Implementation Guidance

Section routing, filename overrides, and sibling-context collection are
deterministic. Role invocation is only for the actual prose generation.

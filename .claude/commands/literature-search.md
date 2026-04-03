# /literature-search

Canonical entrypoint: `pepper literature-search`

## What This Does

Run structured literature search and consolidate the bibliography.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- ensure the target workspace exists and load active target metadata

## Role Steps

- literature-reviewer
- paper-outliner

## Implementation Guidance

Use one or more literature-reviewer tasks to search by topic, method,
data, and venue. Consolidate results into the shared bibliography, then update the stage to
`literature` or `outlining` depending on whether outlining is invoked.

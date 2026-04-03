# /new-paper

Canonical entrypoint: `pepper new-paper`

## What This Does

Scan the repo and initialize a new paper workspace.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- scan the repository using source category patterns from `.pepper/config.yaml`
- create the `paper/` directory structure and state files
- write shared context, claims, figure plan, table plan, and bibliography stubs

## Role Steps

- none

## Implementation Guidance

Use CLI flags or upstream runtime inputs for title, topic, contributions,
venue, and paper type. The CLI owns source-map generation and state-file writes.

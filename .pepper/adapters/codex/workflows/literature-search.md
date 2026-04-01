# literature-search

Canonical entrypoint: `pepper literature-search`

## Summary

Run structured literature search and consolidate the bibliography.

## Deterministic Steps

- ensure the target workspace exists and load active target metadata

## Role Steps

- literature-reviewer
- paper-outliner

## Guidance

Use one or more literature-reviewer tasks to search by topic, method,
data, and venue. Consolidate results into the shared bibliography, then update the stage to
`literature` or `outlining` depending on whether outlining is invoked.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

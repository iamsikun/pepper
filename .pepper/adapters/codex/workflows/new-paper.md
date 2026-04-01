# new-paper

Canonical entrypoint: `pepper new-paper`

## Summary

Scan the repo and initialize a new paper workspace.

## Deterministic Steps

- scan the repository using source category patterns from `.pepper/config.yaml`
- create the `paper/` directory structure and state files
- write shared context, claims, figure plan, table plan, and bibliography stubs

## Role Steps

- none

## Guidance

Use CLI flags or upstream runtime inputs for title, topic, contributions,
venue, and paper type. The CLI owns source-map generation and state-file writes.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

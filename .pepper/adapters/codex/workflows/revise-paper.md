# revise-paper

Canonical entrypoint: `pepper revise-paper`

## Summary

Plan and apply revisions from feedback or updated results.

## Deterministic Steps

- determine revision mode and round number
- persist revision input and backup the current sections

## Role Steps

- revision-planner
- intro-writer
- technical-writer
- empirics-writer

## Guidance

Use the planner to map work first. After user confirmation, invoke only
the required writers, then run deterministic assembly and bookkeeping.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

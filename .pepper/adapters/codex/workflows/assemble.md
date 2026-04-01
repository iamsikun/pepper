# assemble

Canonical entrypoint: `pepper assemble`

## Summary

Build `main.tex` and optionally compile the target paper.

## Deterministic Steps

- read target metadata and section files
- write `paper/<active_target>/main.tex`
- optionally run LaTeX commands when requested

## Role Steps

- none

## Guidance

Assembly should be deterministic. If compilation is requested, use shell
execution but keep manuscript generation itself in the CLI.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

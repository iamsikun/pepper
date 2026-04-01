# create-journal-version

Canonical entrypoint: `pepper create-journal-version`

## Summary

Create a journal target alongside the conference target.

## Deterministic Steps

- create the journal target structure and metadata
- optionally activate the journal target

## Role Steps

- paper-outliner when bootstrap help is needed

## Guidance

The CLI owns the target creation. The outliner is only used when the user
wants a bootstrap outline derived from the conference structure.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

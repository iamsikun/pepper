# /create-journal-version

Canonical entrypoint: `pepper create-journal-version`

## What This Does

Create a journal target alongside the conference target.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- create the journal target structure and metadata
- optionally activate the journal target

## Role Steps

- paper-outliner when bootstrap help is needed

## Implementation Guidance

The CLI owns the target creation. The outliner is only used when the user
wants a bootstrap outline derived from the conference structure.

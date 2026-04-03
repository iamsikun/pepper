# /set-target

Canonical entrypoint: `pepper set-target`

## What This Does

Switch the active paper target.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- validate the target name and update `paper/state.yaml`

## Role Steps

- none

## Implementation Guidance

This workflow is fully deterministic and should not require role help.

# /camera-ready

Canonical entrypoint: `pepper camera-ready`

## What This Does

Prepare the camera-ready package and submission archive.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- copy the assembled manuscript, bibliography, figures, and style assets into the camera-ready directory
- optionally compile and then create `submission.zip`
- update the target stage to `camera-ready`

## Role Steps

- none

## Implementation Guidance

Formatting checks may be aided by a role runtime, but packaging, copying,
and state updates are deterministic CLI work.

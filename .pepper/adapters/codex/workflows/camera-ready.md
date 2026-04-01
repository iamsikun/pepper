# camera-ready

Canonical entrypoint: `pepper camera-ready`

## Summary

Prepare the camera-ready package and submission archive.

## Deterministic Steps

- copy the assembled manuscript, bibliography, figures, and style assets into the camera-ready directory
- optionally compile and then create `submission.zip`
- update the target stage to `camera-ready`

## Role Steps

- none

## Guidance

Formatting checks may be aided by a role runtime, but packaging, copying,
and state updates are deterministic CLI work.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

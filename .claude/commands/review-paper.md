# /review-paper

Canonical entrypoint: `pepper review-paper`

## What This Does

Review the current draft and record a revision plan.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- verify that the target manuscript exists

## Role Steps

- peer-reviewer

## Implementation Guidance

After review completion, update the target stage to `review` and keep the
review output in the target directory.

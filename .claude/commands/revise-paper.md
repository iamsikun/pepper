# /revise-paper

Canonical entrypoint: `pepper revise-paper`

## What This Does

Plan and apply revisions from feedback or updated results.

## How to Execute

1. Run: `pepper workflow-brief revise-paper --guidance "$ARGUMENTS"` to generate a self-contained brief.
2. Read the generated brief at `.pepper/runtime-briefs/revise-paper.md`.
3. Follow the brief's instructions using the embedded section content and session decisions as context.

The brief includes current file content, sibling section labels, and session decisions automatically.
Use `$ARGUMENTS` to pass freeform user guidance (e.g., section name, edit instructions).

## Deterministic Steps

- determine revision mode and round number
- persist revision input and backup the current sections

## Role Steps

- revision-planner
- intro-writer
- technical-writer
- empirics-writer

## Implementation Guidance

Use the planner to map work first. After user confirmation, invoke only
the required writers, then run deterministic assembly and bookkeeping.

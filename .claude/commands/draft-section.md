# /draft-section

Canonical entrypoint: `pepper draft-section`

## What This Does

Draft or revise specific sections with optional custom guidance.

## How to Execute

1. Run: `pepper workflow-brief draft-section --guidance "$ARGUMENTS"` to generate a self-contained brief.
2. Read the generated brief at `.pepper/runtime-briefs/draft-section.md`.
3. Follow the brief's instructions using the embedded section content and session decisions as context.

The brief includes current file content, sibling section labels, and session decisions automatically.
Use `$ARGUMENTS` to pass freeform user guidance (e.g., section name, edit instructions).

## Deterministic Steps

- resolve the requested section names, filenames, and write/revise mode

## Role Steps

- intro-writer
- technical-writer
- empirics-writer

## Implementation Guidance

Section routing, filename overrides, and sibling-context collection are
deterministic. Role invocation is only for the actual prose generation.

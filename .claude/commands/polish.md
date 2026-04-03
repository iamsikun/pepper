# /polish

Canonical entrypoint: `pepper polish`

## What This Does

Copyedit sections for grammar, clarity, and flow without changing content.

## How to Execute

1. Run: `pepper workflow-brief polish --guidance "$ARGUMENTS"` to generate a self-contained brief.
2. Read the generated brief at `.pepper/runtime-briefs/polish.md`.
3. Follow the brief's instructions using the embedded section content and session decisions as context.

The brief includes current file content, sibling section labels, and session decisions automatically.
Use `$ARGUMENTS` to pass freeform user guidance (e.g., section name, edit instructions).

## Deterministic Steps

- resolve target manuscript and section list
- back up current sections before edits

## Role Steps

- copyeditor

## Implementation Guidance

Back up sections before editing. Run the copyeditor on each requested
section. After all edits, do the mandatory post-writing review from writing-style.md:
re-read the full paper to verify internal consistency (notation, terminology, cross-references)
was not broken by the edits.

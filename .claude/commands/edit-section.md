# /edit-section

Canonical entrypoint: `pepper edit-section`

## What This Does

Apply surgical edits to specific sections without rewriting unaffected content.

## How to Execute

1. Run: `pepper workflow-brief edit-section --guidance "$ARGUMENTS"` to generate a self-contained brief.
2. Read the generated brief at `.pepper/runtime-briefs/edit-section.md`.
3. Follow the brief's instructions using the embedded section content and session decisions as context.

The brief includes current file content, sibling section labels, and session decisions automatically.
Use `$ARGUMENTS` to pass freeform user guidance (e.g., section name, edit instructions).

## Deterministic Steps

- resolve the target section file and verify it exists on disk
- collect sibling section labels for cross-reference context

## Role Steps

- intro-writer
- technical-writer
- empirics-writer

## Implementation Guidance

This workflow uses the Edit Mode Protocol from shared-agent-protocols.md.
The user specifies a section file and edit instructions (e.g., line range, paragraph description,
or specific change request). The agent must read the entire file, apply ONLY the requested
changes, and leave all other content byte-identical. Never rewrite paragraphs that are not
mentioned in the edit instructions.

# edit-section

Canonical entrypoint: `pepper edit-section`

## Summary

Apply surgical edits to specific sections without rewriting unaffected content.

## Deterministic Steps

- resolve the target section file and verify it exists on disk
- collect sibling section labels for cross-reference context

## Role Steps

- intro-writer
- technical-writer
- empirics-writer

## Guidance

This workflow uses the Edit Mode Protocol from shared-agent-protocols.md.
The user specifies a section file and edit instructions (e.g., line range, paragraph description,
or specific change request). The agent must read the entire file, apply ONLY the requested
changes, and leave all other content byte-identical. Never rewrite paragraphs that are not
mentioned in the edit instructions.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

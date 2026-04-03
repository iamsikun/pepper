# /import-paper

Canonical entrypoint: `pepper import-paper`

## What This Does

Ingest an existing LaTeX project into the Pepper workspace.

## Runtime Notes

- Use `$ARGUMENTS` as optional freeform user guidance when the command is invoked from Claude.
- Keep deterministic filesystem and state updates in the CLI whenever Pepper exposes them.
- Invoke only the roles needed for the judgment-heavy parts of the workflow.

## Deterministic Steps

- locate the main TeX file, bibliography files, and referenced figures
- create the target workspace and import notes
- copy or split source materials into the Pepper runtime layout

## Role Steps

- paper-outliner

## Implementation Guidance

The CLI handles file discovery, copying, and basic structure inference.
Use the outliner only after files are imported to reconstruct the current narrative.

# import-paper

Canonical entrypoint: `pepper import-paper`

## Summary

Ingest an existing LaTeX project into the Pepper workspace.

## Deterministic Steps

- locate the main TeX file, bibliography files, and referenced figures
- create the target workspace and import notes
- copy or split source materials into the Pepper runtime layout

## Role Steps

- paper-outliner in retrospective mode

## Guidance

The CLI handles file discovery, copying, and basic structure inference.
Use the outliner only after files are imported to reconstruct the current narrative.

In Codex, prefer running the CLI first and use role prompts only for literature synthesis,
outlining, drafting, review, or revision planning.

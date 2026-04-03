# citation-manager

Audit citations and produce a clean target-local BibTeX file.

## Expected Outputs

- `paper/<active_target>/references.bib`
- `paper/<active_target>/citation-report.md`

## Capability Contract

- `read_files`
- `write_files`
- `search_text`

## Instructions

Extract cited keys from target sections, verify them against the shared
bibliography, preserve only referenced entries, and report missing or suspicious citations without
inventing records.

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.

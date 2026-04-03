

<!-- pepper:start -->
# Academic Paper Writing System

Pepper is a project-local academic paper writing framework for machine learning,
economics, marketing, operations research, and quant finance.

The canonical interface is the `pepper` CLI. Runtime adapters such as Claude Code
and Codex consume the same workflow and role definitions rendered into their
preferred local files.

## Canonical Workflows

- `pepper new-paper`
- `pepper import-paper`
- `pepper literature-search`
- `pepper draft-paper`
- `pepper draft-section`
- `pepper edit-section`
- `pepper review-paper`
- `pepper revise-paper`
- `pepper set-target`
- `pepper create-journal-version`
- `pepper assemble`
- `pepper polish`
- `pepper camera-ready`

## Context Resolution

All workflows and roles resolve context through:

1. `paper/state.yaml` for the active target and stage
2. `paper/shared/context.md` for title, topic, contributions, and source map
3. `paper/<active_target>/target.yaml` for venue metadata
4. Repo-local source paths from the source map

Deterministic repo operations belong in the CLI. Role-driven work is reserved for
literature synthesis, outlining, drafting, review, and revision planning.


## Runtime Adapter

This file is the Codex adapter. Treat the `pepper` CLI as the canonical interface for
deterministic repo work. Use the role documents only for judgment-heavy writing and review tasks.

## Workflow Guides

- [new-paper](./.pepper/adapters/codex/workflows/new-paper.md)
- [import-paper](./.pepper/adapters/codex/workflows/import-paper.md)
- [literature-search](./.pepper/adapters/codex/workflows/literature-search.md)
- [draft-paper](./.pepper/adapters/codex/workflows/draft-paper.md)
- [draft-section](./.pepper/adapters/codex/workflows/draft-section.md)
- [edit-section](./.pepper/adapters/codex/workflows/edit-section.md)
- [review-paper](./.pepper/adapters/codex/workflows/review-paper.md)
- [revise-paper](./.pepper/adapters/codex/workflows/revise-paper.md)
- [set-target](./.pepper/adapters/codex/workflows/set-target.md)
- [create-journal-version](./.pepper/adapters/codex/workflows/create-journal-version.md)
- [assemble](./.pepper/adapters/codex/workflows/assemble.md)
- [camera-ready](./.pepper/adapters/codex/workflows/camera-ready.md)
- [polish](./.pepper/adapters/codex/workflows/polish.md)

## Role Guides

- [literature-reviewer](./.pepper/adapters/codex/roles/literature-reviewer.md)
- [paper-outliner](./.pepper/adapters/codex/roles/paper-outliner.md)
- [intro-writer](./.pepper/adapters/codex/roles/intro-writer.md)
- [technical-writer](./.pepper/adapters/codex/roles/technical-writer.md)
- [empirics-writer](./.pepper/adapters/codex/roles/empirics-writer.md)
- [citation-manager](./.pepper/adapters/codex/roles/citation-manager.md)
- [latex-assembler](./.pepper/adapters/codex/roles/latex-assembler.md)
- [venue-formatter](./.pepper/adapters/codex/roles/venue-formatter.md)
- [peer-reviewer](./.pepper/adapters/codex/roles/peer-reviewer.md)
- [revision-planner](./.pepper/adapters/codex/roles/revision-planner.md)
- [copyeditor](./.pepper/adapters/codex/roles/copyeditor.md)
<!-- pepper:end -->

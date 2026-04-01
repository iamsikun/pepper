

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
- `pepper review-paper`
- `pepper revise-paper`
- `pepper set-target`
- `pepper create-journal-version`
- `pepper assemble`
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

This file is the Claude Code adapter. The canonical workflow contract still lives in the
Pepper core spec and the `pepper` CLI.

Use repo-local slash commands as convenience wrappers around the canonical CLI workflows.
When a workflow requires deterministic repository changes, prefer the CLI over ad hoc manual edits.

## Key References

- `.pepper/config.yaml`
- `.pepper/shared-agent-protocols.md`
- `.pepper/writing-style.md`
- `paper/state.yaml`
- `paper/shared/context.md`
- `paper/<active_target>/target.yaml`
<!-- pepper:end -->

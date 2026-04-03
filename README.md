# Academic Paper Writing System

Pepper is an installable CLI scaffold for writing camera-ready academic papers in
machine learning, economics, marketing, operations research, and quant finance.

The core workflow is agent-neutral. Claude Code and Codex are generated adapters
over the same Pepper workflow and role definitions.

## Installation

Install Pepper once as a CLI tool:

```bash
uv tool install git+ssh://git@github.com/<you>/pepper.git --tag v0.1.0
```

Or for local development:

```bash
uv tool install -e /path/to/pepper
```

Then scaffold any research repo:

```bash
pepper install --adapters claude,codex
```

## Canonical Interface

Pepper is CLI-first. These commands are the stable workflow entrypoints:

```bash
# Paper setup
pepper new-paper
pepper import-paper
pepper set-target
pepper create-journal-version

# Writing workflows
pepper literature-search
pepper draft-paper
pepper draft-section
pepper edit-section
pepper review-paper
pepper revise-paper
pepper polish

# Assembly
pepper assemble
pepper camera-ready

# Session state
pepper log-decision "removed tier analysis"
pepper clear-session
pepper sync-context
```

Deterministic repo and state changes happen in the CLI. Judgment-heavy tasks such
as literature synthesis, outlining, drafting, review, and revision planning are
described in generated runtime briefs and role guides.

### Session Decisions Log

Editorial decisions persist across agent calls via a session log. This eliminates
the need to re-state decisions like "we removed tiers" in every prompt:

```bash
pepper log-decision "use stratified sampling, not cluster"
pepper log-decision "renamed DGP 1-4 to descriptive names"
pepper clear-session   # reset between sessions
```

Session decisions are automatically included in workflow briefs and referenced by
all agents via `paper/shared/session-log.md`.

### Section Editing

The `edit-section` and `draft-section` commands support targeted editing:

```bash
pepper edit-section "strengthen motivation" --section introduction
pepper edit-section "fix wording" --section methodology --lines 15-30
pepper draft-section "write the DGP section" --section dgp_model
```

Workflow briefs embed the current section content, sibling section labels, and
session decisions so agents have full context without manual prompting.

## Adapter Outputs

`pepper install --adapters claude,codex` materializes:

```text
your-project/
├── .claude/
│   ├── agents/
│   ├── commands/
│   └── settings.json
├── .pepper/
│   ├── adapters/
│   │   └── codex/
│   │       ├── roles/
│   │       └── workflows/
│   ├── config.yaml
│   ├── shared-agent-protocols.md
│   ├── templates/
│   └── writing-style.md
├── AGENTS.md
└── CLAUDE.md
```

Runtime paper state lives under `paper/` and should be committed:

```text
paper/
├── state.yaml
├── shared/
│   ├── context.md
│   ├── session-log.md
│   ├── claims.md
│   ├── literature/
│   ├── references-master.bib
│   ├── figure-plan.md
│   └── table-plan.md
├── conference/
└── journal/
```

## Typical Flow

Initialize a paper:

```bash
pepper new-paper \
  --title "Optimal Pricing with LLMs" \
  --topic "Dynamic pricing with language-model-assisted demand inference." \
  --contribution "A new demand estimator" \
  --contribution "A policy regret bound" \
  --venue neurips \
  --paper-type "Theory+Experiments"
```

Prepare a literature-search brief for the runtime adapter:

```bash
pepper literature-search --guidance "Focus on dynamic pricing and causal demand estimation."
```

Assemble the current manuscript deterministically:

```bash
pepper assemble
```

Create the camera-ready package:

```bash
pepper camera-ready
```

## Supported Venues

Venue definitions live in `.pepper/config.yaml`. Venue template shells and manifests
live in `.pepper/templates/<venue>/`.

Official `.sty` and `.cls` files are not distributed. Download them from the venue and
place them in the matching template directory before final compilation.

## Development Notes

- Source of truth lives under `src/pepper/`
- Root `.claude/`, `.pepper/`, `CLAUDE.md`, and `AGENTS.md` are generated mirrors
- Use `pepper dev-sync-root` in this repository to refresh the checked-in root mirror

### Syncing changes to project repos

Install pepper in editable mode so source changes are picked up immediately:

```bash
uv tool install -e /path/to/pepper --force
```

Then sync any project repo:

```bash
cd /path/to/project && pepper sync
```

No `--reinstall` or `--force` needed after editable install. Changes to
`core_specs.py`, `renderers.py`, or static assets are reflected on the next
`pepper sync`.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/)
- Claude Code and/or Codex if you want generated runtime adapters
- A LaTeX distribution for compilation
- Venue style files copied into `.pepper/templates/<venue>/`

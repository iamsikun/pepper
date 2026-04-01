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
pepper new-paper
pepper import-paper
pepper literature-search
pepper draft-paper
pepper draft-section
pepper review-paper
pepper revise-paper
pepper set-target
pepper create-journal-version
pepper assemble
pepper camera-ready
```

Deterministic repo and state changes happen in the CLI. Judgment-heavy tasks such
as literature synthesis, outlining, drafting, review, and revision planning are
described in generated runtime briefs and role guides.

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
- Use `pepper sync` in project repos after upgrading the package
- Use `pepper dev-sync-root` in this repository to refresh the checked-in root mirror

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/)
- Claude Code and/or Codex if you want generated runtime adapters
- A LaTeX distribution for compilation
- Venue style files copied into `.pepper/templates/<venue>/`

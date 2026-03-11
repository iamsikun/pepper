# Project-Local Agentic Writer Plan

## Goal

Transform this repository into a **versioned Python package** that stays in a
**private GitHub repository** and installs a **project-local agentic
paper-writing scaffold** into any research repo via `uv`.

The system should feel like a normal per-project tool dependency:

1. Add the private package to a research repo with `uv`.
2. Run a local CLI to install or sync the scaffold files into that repo.
3. Open Claude Code in that repo.
4. Run `/new-paper` and continue the paper workflow locally.
5. Upgrade the package later with `uv`, then re-sync the scaffold.

## Target User Experience

### Recommended flow: tagged releases

```bash
# In a project repo, add a pinned version of the private package
uv add --dev git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.1.0

# Materialize the scaffold into the current repo
uv run pepper install

# Open Claude Code and initialize the paper workspace
claude
/new-paper
```

Upgrade later:

```bash
# Move the repo to a newer tagged version
uv add --dev git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.2.0

# Refresh only package-managed scaffold files
uv run pepper sync
```

### Optional flow: rolling branch

```bash
uv add --dev git+ssh://git@github.com/<you>/<pepper-private-repo>.git --branch stable
uv run pepper install

# Later
uv lock --upgrade-package pepper
uv run pepper sync
```

Tagged releases are the default recommendation. They are easier to reason about
and safer when multiple research repos are active at once.

## Desired End State

The system should model:

- one repository = one research project
- one `paper/` directory = one manuscript family for that project
- up to two paper targets: `paper/conference/` and `paper/journal/`
- one private `pepper` repo = reusable framework source
- one pinned `pepper` version per project repo via `pyproject.toml` and `uv.lock`

The system should not require:

- symlinks into a central scaffold repo
- manual copy-paste updates across repos
- a public PyPI package
- a central hub repo that tracks active projects
- project-specific state baked into the package itself

## Core Design Principles

### 1. Project-local runtime

All manuscript state and all Claude-facing working files must live inside the
active research repo. The repo is the project.

### 2. Package-managed scaffold

The reusable framework is distributed as a Python package. The package ships the
scaffold assets and a CLI that installs or syncs those assets into a target repo.

### 3. Explicit file ownership

The package manages scaffold files. The user manages manuscript state. Sync logic
must know which files it owns and must avoid touching runtime paper content.

### 4. Reproducible upgrades

Each project pins a package version. Upgrades happen deliberately through `uv`,
not by re-running an arbitrary shell script from a mutable checkout.

### 5. Private by default

The package remains in a private GitHub repo for now. Installation and upgrade
must work cleanly through private Git dependencies.

### 6. Share evidence, not prose

Conference and journal targets share research truth, claims, evidence,
bibliography, and figure/table plans. They do not share raw section prose.

### 7. Commit manuscript state

`paper/` is core project state, not disposable runtime cache. Drafts, outlines,
references, reviews, and workflow state should be committed. Only generated build
artifacts should be gitignored.

## What Changes Relative To The Old Plan

The old copy-based installer is no longer the primary contract.

Replace this:

- "run `install.sh` from the scaffold repo into a target repo"

With this:

- "add `pepper` to the target repo with `uv`"
- "run `uv run pepper install`"
- "upgrade with `uv`, then run `uv run pepper sync`"

The package CLI becomes the installer. Any shell scripts that remain are optional
wrappers only and must not be the main distribution mechanism.

## Package Architecture

The private source repo should become a normal Python package with packaged
scaffold assets.

### Package repo layout

```text
pepper-repo/
├── pyproject.toml
├── README.md
├── src/
│   └── pepper/
│       ├── __init__.py
│       ├── cli.py
│       ├── sync.py
│       ├── validate.py
│       ├── manifest.py
│       └── assets/
│           ├── .claude/
│           │   ├── agents/
│           │   ├── commands/
│           │   └── settings.json
│           ├── .pepper/
│           │   ├── config.yaml
│           │   └── templates/
│           └── CLAUDE.template.md
└── tests/
```

### Packaging rules

- Scaffold assets are shipped as package data under `src/pepper/assets/`
- CLI reads assets with `importlib.resources`
- The package exposes a console script named `pepper`
- The package version in `pyproject.toml` is the scaffold version installed into
  each project repo

## Installed Files In A Project Repo

After `uv run pepper install`, a target repo should look like this:

```text
project-root/
├── .claude/
│   ├── agents/
│   ├── commands/
│   └── settings.json
├── .pepper/
│   ├── config.yaml
│   ├── templates/
│   └── install-manifest.json
├── CLAUDE.md
└── paper/
    ├── state.yaml
    ├── shared/
    ├── conference/
    └── journal/
```

### File ownership

Package-managed files:

- `.claude/**`
- `.pepper/config.yaml`
- `.pepper/templates/**`
- `.pepper/install-manifest.json`
- the package-managed block inside `CLAUDE.md`

User-managed runtime files:

- `paper/**`
- user-authored content in `CLAUDE.md` outside the managed block
- the repo's normal code, docs, data, experiment outputs, and figures

## Claude Integration Contract

Claude Code expects commands and agent prompts to exist locally in the current
repo. The package therefore must **materialize real files** into the target repo;
it must not rely on symlinks or remote references.

The Claude-facing commands remain the same:

- `/new-paper`
- `/set-target`
- `/literature-search`
- `/draft-paper`
- `/review-paper`
- `/camera-ready`
- `/create-journal-version`

The `pepper` CLI does not replace those commands. It installs and updates the
files that define those commands.

## Runtime Manuscript Model

The project-local manuscript model from the earlier plan still applies.

### Runtime layout

```text
paper/
├── state.yaml
├── shared/
│   ├── context.md
│   ├── claims.md
│   ├── literature/
│   ├── references-master.bib
│   ├── figure-plan.md
│   ├── table-plan.md
│   └── evidence/
├── conference/
│   ├── target.yaml
│   ├── outline.md
│   ├── sections/
│   ├── figures/
│   ├── references.bib
│   ├── main.tex
│   ├── review.md
│   ├── revision-plan.md
│   └── camera-ready/
└── journal/
    ├── target.yaml
    ├── outline.md
    ├── sections/
    ├── figures/
    ├── references.bib
    ├── main.tex
    ├── review.md
    ├── revision-plan.md
    └── submission/
```

### Source map contract

`/new-paper` scans the current repo and writes a source map into
`paper/shared/context.md`. Agents read the source map rather than hardcoding
paths like `src/`, `docs/`, or `results/`.

The source map is still the bridge between an arbitrary research repo and the
paper-writing agents.

## CLI Contract

The initial package CLI should expose these commands:

### `pepper install`

Purpose:

- install scaffold files into the current repo
- create `.pepper/install-manifest.json`
- initialize managed blocks in `CLAUDE.md`
- add recommended ignore rules for generated paper build artifacts

Behavior:

- safe to run in a fresh repo
- safe to re-run if the scaffold is already installed
- must not create or modify `paper/` content except where explicitly requested by
  Claude slash commands later

### `pepper sync`

Purpose:

- update scaffold files in the current repo from the currently installed package
  version

Behavior:

- overwrite unchanged managed files
- update the managed block in `CLAUDE.md`
- leave all `paper/` content untouched
- detect local edits to managed scaffold files and refuse to overwrite them by
  default
- support a `--force` flag to overwrite managed-file conflicts when the user
  explicitly wants that behavior

### `pepper validate`

Purpose:

- validate scaffold integrity and runtime paper structure

Checks:

- path lint for banned legacy path references
- template manifest presence
- state validation if `paper/` exists
- target directory validation
- section lint for unresolved LaTeX markers or `TODO`s in camera-ready stage

### `pepper version`

Purpose:

- print the package version
- print the installed scaffold version recorded in
  `.pepper/install-manifest.json`
- report whether the current repo is in sync with the package version

## Sync Engine Contract

The sync implementation is the core of this design.

### Manifest

`install-manifest.json` should record:

- installed scaffold version
- the list of package-managed files
- content hashes for those files
- the last sync timestamp

### Default sync behavior

For each managed file:

- if the file does not exist locally, create it
- if the file matches the last installed hash, replace it with the new package version
- if the file differs from the manifest hash, treat it as a local modification and
  report a conflict

### `CLAUDE.md` handling

`CLAUDE.md` should be managed only inside explicit markers, for example:

```md
<!-- pepper:start -->
[package-managed instructions]
<!-- pepper:end -->
```

Anything outside those markers is user-owned and must be preserved across syncs.

### `.gitignore` handling

The installer should manage a small, marked block in `.gitignore` for generated
paper build outputs only. It should not add `paper/` itself to `.gitignore`.

Recommended ignore entries:

- `paper/**/camera-ready/`
- `paper/**/submission/`
- `paper/**/*.aux`
- `paper/**/*.bbl`
- `paper/**/*.blg`
- `paper/**/*.fdb_latexmk`
- `paper/**/*.fls`
- `paper/**/*.log`
- `paper/**/*.out`
- `paper/**/*.synctex.gz`

## Versioning And Release Model

### Source of truth

The private `pepper` repo is the source of truth for scaffold code and assets.

### Versioning

- use semantic-ish version tags such as `v0.1.0`, `v0.2.0`
- the package version and the Git tag should match
- each project repo pins either a tag or a branch in `pyproject.toml` and
  `uv.lock`

### Recommendation

- use tags for normal research repos
- use a `stable` branch only when you intentionally want rolling updates

### Authentication

Private Git installation should work through:

- SSH keys with `git+ssh://git@github.com/...`
- or Git credential helper-backed HTTPS if needed

The plan should assume SSH is the default path for local development.

## Template Distribution

Template manifests and package-owned template skeletons should be distributed as
package assets.

If venue `.sty` or `.cls` files cannot be redistributed, the package should ship:

- the template directory structure
- `template-manifest.yaml`
- clear placeholder instructions for which upstream files the user must download

## Prompt And Path Contract

All command and agent prompts must follow the project-local path model:

- no `projects/`
- no `papers/`
- no `workspace/`
- no `current-paper.md`
- no legacy `literature/` path assumptions

Project context must come from:

- `paper/state.yaml`
- `paper/shared/context.md`
- `paper/<target>/target.yaml`
- source map entries listed in `paper/shared/context.md`

## Git Policy For `paper/`

Commit:

- `paper/state.yaml`
- `paper/shared/**`
- `paper/<target>/target.yaml`
- `paper/<target>/outline.md`
- `paper/<target>/sections/**`
- `paper/<target>/figures/**`
- `paper/<target>/references.bib`
- `paper/<target>/main.tex`
- `paper/<target>/review.md`
- `paper/<target>/revision-plan.md`

Ignore:

- generated submission bundles
- LaTeX intermediate files
- any local scratch files explicitly created as temporary working output

## Implementation Phases

## Phase 1: Package skeleton

### Objective

Turn this repo into a Python package with a CLI entry point.

### Tasks

- add `pyproject.toml`
- create `src/pepper/`
- add console entry point for `pepper`
- add package data configuration for scaffold assets
- add minimal tests for package import and CLI entry point

### Exit criteria

- `uv run pepper version` works in this repo
- package assets are readable via `importlib.resources`

## Phase 2: Install and sync engine

### Objective

Implement deterministic scaffold installation and upgrades.

### Tasks

- implement repo-root detection
- implement asset enumeration
- implement manifest read/write
- implement file hashing
- implement managed-file install
- implement conflict detection for locally modified managed files
- implement `CLAUDE.md` marker updates
- implement `.gitignore` marker updates

### Exit criteria

- `pepper install` works in a clean test repo
- `pepper sync` updates managed files without touching `paper/`
- local modifications to managed files are detected correctly

## Phase 3: Migrate scaffold assets into the package

### Objective

Make packaged assets the only source for Claude commands, agents, config, and templates.

### Tasks

- move `.claude/` into `src/pepper/assets/.claude/`
- move reusable `.pepper/` assets into `src/pepper/assets/.pepper/`
- convert `CLAUDE.md` into a template or managed block source
- remove copy-installer-first assumptions from docs and code

### Exit criteria

- installing from the package materializes all required scaffold files
- no core workflow depends on a checked-out scaffold repo

## Phase 4: Prompt migration to the project-local model

### Objective

Update every command and agent prompt to the new path contract.

### Tasks

- update `/new-paper`
- update `/literature-search`
- update `/draft-paper`
- update `/camera-ready`
- update all agents to read from the source map and `paper/<target>/...`
- run path lint after each prompt update

### Path lint

Fail the phase if any prompt file still references:

- `projects/`
- `papers/`
- `workspace/`
- `current-paper.md`
- legacy literature paths

### Exit criteria

- no prompt references legacy paths
- all prompts follow the source-map-based project-local contract

## Phase 5: Validation and tests

### Objective

Catch regressions in packaging, sync, and prompt contracts.

### Tasks

- implement `pepper validate`
- add tests for install on a fresh repo
- add tests for sync on an upgraded package version
- add tests for `CLAUDE.md` preservation outside managed markers
- add tests for manifest conflict detection
- add tests for path lint

### Exit criteria

- validation passes on a clean installed scaffold
- validation catches at least one known regression in prompts or runtime state

## Phase 6: Private-repo release workflow

### Objective

Make the package practical to use across multiple private research repos.

### Tasks

- document the private Git `uv add --dev` workflow
- document tagged release workflow
- document branch-based workflow as optional
- document SSH authentication expectations
- test install and upgrade from a separate sample repo

### Exit criteria

- a separate private project repo can install from a tag
- that repo can upgrade to a newer tag and run `pepper sync`

## Acceptance Criteria

The implementation is complete when:

1. This repo is a working Python package with a `pepper` CLI.
2. A separate project repo can install the private package with `uv add --dev`.
3. `uv run pepper install` materializes the scaffold into a clean project repo.
4. `uv run pepper sync` updates only package-managed scaffold files.
5. `paper/` runtime content is never modified by install or sync.
6. `CLAUDE.md` content outside managed markers is preserved across syncs.
7. Local modifications to managed scaffold files are detected and reported.
8. All prompts follow the project-local path contract and use the source map.
9. The recommended gitignore block ignores build artifacts, not the whole `paper/`
   tree.
10. A project pinned to `v0.1.0` can be upgraded to `v0.2.0` via `uv`, then
    re-synced successfully.

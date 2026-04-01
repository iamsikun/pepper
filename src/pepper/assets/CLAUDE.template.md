# Academic Paper Writing System

## Researcher Profile

**Domains:** Machine Learning, Marketing, Econometrics, Operations, Quant Finance
**Target Venues:** Configured per-project in `.pepper/config.yaml`

---

## System Architecture

This system uses a pipeline of specialized subagents to produce camera-ready academic papers:

```
[/new-paper] ─────────┐
                       ↓
[/import-paper] → paper-outliner ──→ (retrospective outline)
                       ↓
       ┌───────────────┼───────────────┐
  intro-writer   technical-writer  empirics-writer
       └───────────────┼───────────────┘
                       ↓
            citation-manager
                       ↓
            latex-assembler
                       ↓
            venue-formatter
                       ↓
            peer-reviewer
                  ↓    ↑
          revision-planner ←─ /revise-paper
                  ↓
       selective writer re-invocation
                  ↓
         [camera-ready output]
```

Pipeline state is tracked in `paper/state.yaml`. Each target (conference/journal) has its own stage: `init` → `literature` → `outlining` → `drafting` → `review` → `revising` → `camera-ready` → `done`

`/new-paper` feeds into the full pipeline. `/import-paper` enters mid-stream (Review → `drafting`, Revise → `outlining`, Retarget → `drafting`).

---

## Target Resolution Protocol

All agents and commands resolve their context through these files:

1. **`paper/state.yaml`** → `active_target` (conference or journal) + per-target stage
2. **`paper/shared/context.md`** → title, topic, contributions, paper type, **source map**
3. **`paper/<active_target>/target.yaml`** → venue, template, mode, page_limit, audience
4. **Source map paths** → project-specific locations for docs, code, results, data

Agents must NOT hardcode paths. If a source map path is missing, note the gap and proceed.

Full context resolution steps are in `.pepper/shared-agent-protocols.md`.

---

## Paper Management

### Shared vs Target-Specific

**Shared** (`paper/shared/`): problem framing, claims, evidence, literature, bibliography, figure/table plans. These are the research truth — shared across targets.

**Target-specific** (`paper/<target>/`): section prose, outline, assembled paper, review feedback. Never share raw section text between targets.

### Source Map

The repository IS the project. `/new-paper` scans the repo and writes a source map into `paper/shared/context.md`. Agents read source map paths rather than guessing.

---

## Key References

- **Writing conventions:** `.pepper/writing-style.md` — notation, venue styles, universal rules
- **Agent protocols:** `.pepper/shared-agent-protocols.md` — context resolution, revision mode, selective section mode
- **Venue config:** `.pepper/config.yaml` — venues, page limits, bib styles
- **Templates:** `.pepper/templates/<venue>/` — LaTeX templates and manifests

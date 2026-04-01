# Pepper Prompt Cleanup — Refactoring Tracker

## Goal

Reduce ~4,500 lines of prompt content by ~30% by consolidating duplicated instructions into shared reference files and trimming each agent/command to essential-only content.

## Architecture Note

All edits go to `src/pepper/assets/` (source of truth), then sync to root `.claude/`/`.pepper/`.

---

## Phase 1: Create shared reference files
- [x] 1a. Expand `.pepper/writing-style.md` — add notation standards, venue styles, citation conventions
- [x] 1b. Create `.pepper/shared-agent-protocols.md` — context resolution, revision mode, selective section mode
- [x] 1c. Sync new files to root `.pepper/`

## Phase 2: Slim down agents (980 → 747 lines, -24%)
- [x] Remove Context Resolution block from all 10 agents → one-line reference
- [x] Remove Revision Mode block from 3 writer agents → one-line reference + agent-specific bullets only
- [x] Remove Selective Section Mode block from 3 writer agents → one-line reference
- [x] Remove venue-style guidance that duplicates writing-style.md
- [x] Remove Mathematical Notation Standards from technical-writer (now in writing-style.md)

## Phase 3: Merge `/revise-paper` and `/update-results` (180 → 106 lines, -41%)
- [x] Merge into single `/revise-paper` with mode detection
- [x] Remove `/update-results` command

## Phase 4: Deduplicate `/new-paper` and `/import-paper` (362 → 244 lines, -33%)
- [x] `/import-paper` references `/new-paper` for shared patterns (state files, dirs, source map)
- [x] Tightened `/import-paper` prose (230 → 111 lines)

## Phase 5: Trim CLAUDE.md (220 → 82 lines, -63%)
- [x] Remove full directory tree (agents discover this)
- [x] Move venue writing guidelines to writing-style.md (done in Phase 1)
- [x] Remove detailed revision workflow (lives in commands)
- [x] Remove pipeline stages list (merged into architecture section)
- [x] Keep: pipeline diagram, target resolution, shared-vs-target, source map concept
- [x] Add "Key References" section pointing to writing-style.md, shared-agent-protocols.md, config.yaml

## Phase 6: Clean up settings.local.json (43 → 18 lines)
- [x] Remove stale paths from before the rename (Desktop/research/paper-writer, .paperwriter)
- [x] Remove one-off permission entries accumulated during development
- [x] Consolidate to clean, general-purpose permissions

---

## Final Summary

| Component | Before | After | Change |
|---|---|---|---|
| 10 agents | 980 | 747 | -24% |
| 11 → 10 commands | 1,037 | 845 | -19% |
| CLAUDE.template.md | 222 | 78 | -65% |
| writing-style.md | 34 | 74 | +118% (absorbs content) |
| shared-agent-protocols.md | 0 | 50 | new |
| settings.local.json | 43 | 21 | -51% |
| **Net total** | 2,316 | 1,815 | **-22%** |

New shared reference files (+124 lines) enable the reductions everywhere else (-625 lines).

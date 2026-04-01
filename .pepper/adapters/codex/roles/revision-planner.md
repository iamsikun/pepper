# revision-planner

Map review feedback or updated results to concrete section-level changes.

## Expected Outputs

- `paper/<active_target>/revisions/round-<N>/revision-plan.md`

## Capability Contract

- `read_files`
- `write_files`

## Instructions

Read the revision input, existing sections, outline, and shared claims.
Produce a per-section action map with explicit agent ownership, minimal scope, prerequisites, and
cross-section consistency notes. Every review comment must be mapped or explicitly rejected.

Use the canonical Pepper CLI workflows whenever deterministic repo or state changes are needed.

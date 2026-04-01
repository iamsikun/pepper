# Shared Agent Protocols

Protocols referenced by multiple agents. Read this file when an agent prompt directs you here.

---

## Context Resolution Protocol

All agents resolve their working context through these steps:

1. Read `paper/state.yaml` → get `active_target` (conference or journal) and per-target stage
2. Read `paper/shared/context.md` → title, topic, contributions, paper type, and **source map**
3. Read `paper/<active_target>/target.yaml` → venue, template, mode, page_limit, audience
4. For project materials, follow source map paths from context.md. Do not hardcode paths. Note gaps if paths are missing and proceed with available information.

---

## Selective Section Mode Protocol

When invoked by `/draft-section`, the orchestrator specifies:
- **Sections to write:** a subset of the agent's file list — write ONLY these
- **Custom guidance:** additional user instructions — follow these as priority directives
  that override default emphasis, scope, and style choices (but not correctness rules)
- **Sibling sections:** read-only `.tex` content from other sections for cross-referencing

If the target section file already exists on disk, operate in **revise mode**: read the
existing content first, preserve what works, and improve or restructure as directed by
the custom guidance. If the file does not exist, write from scratch using the outline.

If no selective section parameters are provided (i.e., invoked by `/draft-paper`),
write all sections listed in the agent's file list.

---

## Revision Mode Protocol

When `paper/<active_target>/revisions/round-<N>/revision-plan.md` exists and the agent is
invoked by `/revise-paper` or `/update-results`, operate in revision mode:

1. **Read existing:** Always read the EXISTING `.tex` files first — never start from scratch
2. **Scope:** Only change what the revision plan specifies for this agent. Do not rewrite
   sections that are marked NO_CHANGE.
3. **Action types:**
   - MINOR_EDIT → surgical edits (fix a sentence, add a citation, adjust wording)
   - MAJOR_REVISION → rewrite larger portions but preserve overall structure unless the
     revision plan says otherwise
4. **Traceability:** Add `% REVISED: <note>` LaTeX comments next to substantive changes

Each writer agent may have additional agent-specific revision rules (e.g., updating tables,
propagating assumption changes). Follow those in addition to the rules above.

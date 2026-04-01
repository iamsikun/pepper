# /draft-section

Draft or revise specific paper section(s) with optional custom instructions.

## What This Does

Parses freeform instructions to determine which section(s) to write or revise, routes
to the correct writer agent(s), and passes custom guidance through. Unlike `/draft-paper`,
this does NOT reassemble the paper or run citation-manager afterward.

## Input Resolution

`$ARGUMENTS` contains the user's freeform instructions.

Parse the text to determine:
1. **Which section(s)** to draft — match against the Section Routing Table below
2. **Custom guidance** — any remaining text beyond the section name(s) is treated as
   additional instructions passed to the writer agent

If `$ARGUMENTS` is empty, respond with:

> Which section(s) would you like me to draft? You can say things like:
> - `methodology`
> - `introduction and related work`
> - `rewrite the abstract to be more concise`
> - `experiments section focusing on ablation studies`
>
> Run `/draft-paper` to draft all sections at once.

Do NOT proceed with any agent invocation when arguments are empty.

## Section Routing Table

| Aliases | Canonical file | Agent |
|---|---|---|
| abstract | `abstract.tex` | intro-writer |
| introduction, intro | `introduction.tex` | intro-writer |
| related work, literature review, prior work | `related_work.tex` | technical-writer |
| background, preliminaries, setup | `background.tex` | technical-writer |
| methodology, method, model, approach | `methodology.tex` | technical-writer |
| theory, theoretical analysis | `theory.tex` | technical-writer |
| appendix proofs, proofs | `appendix_proofs.tex` | technical-writer |
| experiments, results, evaluation, empirics, empirical | `experiments.tex` (ML) or `empirics.tex` (econ) | empirics-writer |
| appendix experiments, additional experiments | `appendix_experiments.tex` | empirics-writer |
| conclusion, conclusions, discussion | `conclusion.tex` | technical-writer |

Use fuzzy, case-insensitive matching. If the user's text does not clearly match any
section, ask for clarification before proceeding.

## Filename Override

Users can specify a custom output filename using the syntax:

```
<section_name> as <filename.tex>
```

Examples:
- `methodology as dgp_model.tex` — routes to technical-writer but outputs `dgp_model.tex`
- `experiments as monte_carlo.tex` — routes to empirics-writer but outputs `monte_carlo.tex`

The routing table still determines which agent handles the section. Only the output
filename changes.

**Parsing rule:** If `$ARGUMENTS` contains ` as ` followed by a `.tex` filename,
extract the filename as the override. The text before ` as ` is matched against the
routing table. Any text after the filename is treated as custom guidance.

If no explicit override is specified, also check `paper/<active_target>/outline.md`
for custom filenames in the section plan (sections annotated with
`(filename: X.tex)`). Priority order: explicit `as` override > outline annotation >
canonical filename.

## Prerequisites

1. Read `paper/state.yaml` → get `active_target` and verify stage is at least `outlining`.
   If not, stop and tell the user to run `/literature-search` first.
2. Read `paper/<active_target>/outline.md` → confirm the outline exists.
3. Read `paper/shared/context.md` → get title, contributions, source map.

## Determining Write vs Revise Mode

For each resolved section:
- If `paper/<active_target>/sections/<file>.tex` exists → **Revise mode**.
  The agent reads existing content, preserves what works, improves what the guidance targets.
- If the file does not exist → **Write mode**.
  The agent writes from scratch using the outline as blueprint.

Report the mode to the user before dispatching: "Writing methodology (new) and
revising introduction (exists)."

## Gathering Sibling Context

Before invoking agents, read all EXISTING `.tex` files in
`paper/<active_target>/sections/` that are NOT being written/revised in this invocation.
Pass their content to the agent(s) as read-only sibling context for cross-referencing
and consistency.

## Conclusion Special Handling

If the user requests the conclusion:
- If other sections are also requested in the same invocation, write those first,
  then write the conclusion after they complete (the conclusion references the full paper).
- If only the conclusion is requested, read all existing sibling sections as context.
- Warn the user if fewer than 3 sibling sections exist: "Note: only N other sections exist.
  The conclusion may need revision after more sections are drafted."

## Agent Dispatch

Group resolved sections by agent. For each agent that has work:

1. Invoke the agent with these parameters in its prompt:
   - **Sections to write:** list of resolved output filenames (canonical, outline-overridden,
     or user-overridden via `as` syntax)
   - **Mode per section:** WRITE or REVISE
   - **Custom guidance:** the user's additional instructions extracted from `$ARGUMENTS`
   - **Sibling sections:** read-only content of other existing `.tex` files
2. If sections map to multiple different agents, invoke them **in parallel**
3. Exception: conclusion always runs after all other requested sections complete

## State Management

Do NOT update `paper/state.yaml` stage. Section-level drafting does not change the
pipeline stage — that is handled by `/draft-paper` and `/camera-ready`.

## Reporting

After agent(s) complete, tell the user:
- Which sections were written or revised
- Write vs Revise mode for each
- Any `% TODO` placeholders inserted
- Suggested next steps (e.g., "Run `/draft-paper` to assemble" or "Run `/review-paper`
  to get feedback on the updated sections")

# /literature-search

Run a comprehensive literature search for the current paper.

## What This Does

Invokes the `literature-reviewer` agent to search for relevant academic papers,
synthesize the findings, and populate the bibliography.

## Instructions

1. Read `paper/shared/context.md` to get the topic and contributions.
2. Read `paper/state.yaml` to confirm the active target and current stage.

3. Use the `literature-reviewer` subagent to:
   - Search for papers on the main topic
   - Search for papers on each key method or dataset used
   - Search for papers at the target venue in the same area
   - Find the key baselines the paper will compare against

4. For papers that span multiple themes, spawn multiple `literature-reviewer` agents
   in parallel — one per research thread:

   Example for an ML paper on "robust optimization for bandits":
   - Agent 1: "robust optimization machine learning"
   - Agent 2: "bandit algorithms exploration exploitation"
   - Agent 3: "distributionally robust optimization"

5. After the agents complete:
   - Consolidate all BibTeX into `paper/shared/references-master.bib`
   - Update `paper/state.yaml` to set the active target's stage to `literature`

6. Ask the user: "Literature review is complete. I found [N] papers.
   Key gaps identified: [list].
   Shall I proceed with paper outlining?"

7. If yes, invoke the `paper-outliner` agent. After outliner completes,
   update `paper/state.yaml` to set the active target's stage to `outlining`.

## Parallel Search Strategy

For ML papers, search simultaneously:
- Core method (e.g., "contrastive learning")
- Application domain (e.g., "medical imaging")
- Theoretical tools used (e.g., "PAC learning bounds")

For econ/marketing papers, search simultaneously:
- Main topic (e.g., "dynamic pricing")
- Empirical strategy (e.g., "regression discontinuity")
- Applied domain (e.g., "airline revenue management")

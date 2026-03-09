# /literature-search

Run a comprehensive literature search for the current paper.

## What This Does

Invokes the `literature-reviewer` agent to search for relevant academic papers,
synthesize the findings, and populate the bibliography.

## Instructions

1. Read `workspace/current-paper.md` to get the topic and contributions.

2. Use the `literature-reviewer` subagent to:
   - Search for papers on the main topic
   - Search for papers on each key method or dataset used
   - Search for papers at the target venue (NeurIPS/ICML/etc.) in the same area
   - Find the key baselines the paper will compare against

3. For papers that span multiple themes, spawn multiple `literature-reviewer` agents
   in parallel — one per research thread:
   
   Example for an ML paper on "robust optimization for bandits":
   - Agent 1: "robust optimization machine learning"
   - Agent 2: "bandit algorithms exploration exploitation"  
   - Agent 3: "distributionally robust optimization"

4. After the agents complete:
   - Consolidate all BibTeX into `research/literature/references.bib`
   - Update `workspace/current-paper.md` to check off literature review

5. Ask the user: "Literature review is complete. I found [N] papers.
   Key gaps identified: [list].
   Shall I proceed with paper outlining?"

6. If yes, invoke the `paper-outliner` agent.

## Parallel Search Strategy

For ML papers, search simultaneously:
- Core method (e.g., "contrastive learning")
- Application domain (e.g., "medical imaging")
- Theoretical tools used (e.g., "PAC learning bounds")

For econ/marketing papers, search simultaneously:
- Main topic (e.g., "dynamic pricing")
- Empirical strategy (e.g., "regression discontinuity")
- Applied domain (e.g., "airline revenue management")

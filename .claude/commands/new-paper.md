# /new-paper

Initialize a new paper project. Run this first before any other commands.

## What This Does

Sets up the workspace for a new paper, captures key information, and prepares the
directory structure for the full pipeline.

## Instructions

First, ask the user if this paper isconnected to an existing project in `projects/`? If yes, which one?
Then, scan the `/docs/` folder in that project for `context.md`. 
If there is one, find the answers to the following questions from `context.md`: 
1. **Paper Title** (working title is fine)
2. **Research Topic** — 2–3 sentence description of what the paper is about
3. **Key Contributions** — what are the 2–4 main things this paper claims to do/show/prove?
4. **Target Venue** — one of: NeurIPS, ICML, ICLR, Econometrica, Marketing Science, Management Science
5. **Paper Type** — Modeling / Theory / Empirical / Theory+Experiments / Methodology
6. **Connected Project** - which project symlink is related to this 

If there are no answers to these questions or the answers are not clear, ask the users. 


Then, create the structure specified in the paper management section from CLAUDE.md. 

Finally, write the `papers/<slug>/workspace/current-paper.md` file with this template:

```markdown
# Current Paper

## Metadata
- **Title:** [title]
- **Slug:** [slug]
- **Venue:** [venue]
- **Type:** [type]
- **Created:** [today's date]

## Research Topic
[2–3 sentences]

## Key Contributions
1. [Contribution 1 — be specific]
2. [Contribution 2]
3. [Contribution 3]

## Pipeline Status
- [ ] Literature review (`/literature-search`)
- [ ] Paper outline (`paper-outliner` agent)
- [ ] Introduction + Abstract (`intro-writer` agent)
- [ ] Technical sections (`technical-writer` agent)
- [ ] Experiments/Empirics (`empirics-writer` agent)
- [ ] Citations (`citation-manager` agent)
- [ ] Assembly (`latex-assembler` agent)
- [ ] Venue formatting (`venue-formatter` agent)
- [ ] Peer review (`peer-reviewer` agent)
- [ ] Camera-ready (`/camera-ready`)

## File Locations
- Sections: `papers/<slug>/workspace/sections/`
- Literature: `literature/`
- Assembled: `papers/<slug>/main.tex`
- Camera-ready: `papers/<slug>/camera-ready/`

## Notes
[Any special instructions or constraints for this paper]
```

7. Confirm setup is complete and tell the user to run `/literature-search` next.

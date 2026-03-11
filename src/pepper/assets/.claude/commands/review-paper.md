# /review-paper

Run a simulated peer review on the active paper target.

## What This Does

Invokes the `peer-reviewer` agent to provide structured feedback on the current draft,
identifying strengths, weaknesses, and required revisions.

## Instructions

1. Read `paper/state.yaml` to get the active target.

2. Verify that `paper/<active_target>/main.tex` exists. If not, tell the user to run
   `/draft-paper` first.

3. Invoke the `peer-reviewer` agent on the active target. The agent will:
   - Read the assembled paper or section files
   - Produce a detailed review at `paper/<active_target>/review.md`
   - Produce a revision plan at `paper/<active_target>/revision-plan.md`

4. Update `paper/state.yaml` to set the active target's stage to `review`.

5. Present a summary of the review to the user:
   - Overall score/recommendation
   - Top 3 strengths
   - Top 3 weaknesses
   - Number of critical vs. important vs. minor issues

6. Ask: "Would you like to address any of these issues now? I can invoke the relevant
   section-writing agents to make revisions."

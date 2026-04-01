# /camera-ready

Prepare the final camera-ready submission package for the target venue.

## What This Does

Takes the assembled paper through final formatting, verification, and packaging
to produce a submission-ready package.

## Custom Instructions

`$ARGUMENTS` contains optional freeform guidance from the user.

If non-empty, incorporate this guidance into the formatting and packaging steps. Examples:
- "use the updated author list in authors.txt" → read that file for author info
- "add acknowledgments: NSF grant #12345" → include in acknowledgments section
- "skip anonymization, this is camera-ready" → set mode accordingly
- "check that all figures are at least 300 DPI" → add to visual inspection

If empty, proceed with default behavior.

## Prerequisites

Read `paper/state.yaml` to get the active target.
Verify:
- `paper/<active_target>/main.tex` exists and compiles
- `paper/<active_target>/references.bib` is complete
- User has confirmed all TODO placeholders are resolved

If TODOs remain, alert the user and list them. Ask for confirmation before proceeding.

## Pipeline

### Step 1: Final Citation Check
Invoke `citation-manager` one final time:
- Check for any new citations added during revision
- Verify all arXiv entries against published versions
- Ensure DOIs are present

### Step 2: Venue Formatting
Invoke `venue-formatter` to:
- Apply the correct year's style file from `.pepper/templates/<venue>/`
- Check page limits (count carefully!)
- Add/remove anonymization as appropriate
- Add acknowledgments section (camera-ready only)
- Add venue-specific checklist (if required by venue)
- Verify figure resolution

### Step 3: Final Compilation
```bash
cd paper/<active_target>/camera-ready
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Check compilation log for:
- Errors (must fix all)
- Warnings (fix overfull hboxes)
- Page count (must be within limit)

### Step 4: Visual Inspection Checklist
Read through the compiled PDF and verify:

```markdown
## Visual Inspection

### First Pages
- [ ] Title looks correct
- [ ] Author list correct (camera-ready) or anonymous (blind)
- [ ] Abstract is within word limit
- [ ] Introduction starts on correct page

### Body
- [ ] Section numbering is correct
- [ ] All figures appear, are readable, and have captions
- [ ] All tables appear, are formatted properly
- [ ] All equations are properly formatted
- [ ] Theorem/Lemma/Proposition boxes appear correctly
- [ ] Algorithm box appears correctly

### References
- [ ] Bibliography appears
- [ ] Citations in text match bibliography
- [ ] No "[?]" references (unresolved citations)

### Appendix
- [ ] Appendix appears after references (or before, per venue)
- [ ] Appendix is labeled A, B, C... not 1, 2, 3

### Page Count
- [ ] Main body: [X] pages (limit: [Y])
- [ ] Total with appendix: [Z] pages
```

### Step 5: Create Submission Package

```bash
cd paper/<active_target>/camera-ready
zip -r ../submission.zip main.tex references.bib *.sty *.cls figures/
```

Report: "Camera-ready package created at `paper/<active_target>/submission.zip`.
Page count: [N]/[limit]. Ready for submission to [venue]."

### Step 6: Update State

Update `paper/state.yaml` to set the active target's stage to `camera-ready`.

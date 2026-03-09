# /camera-ready

Prepare the final camera-ready submission package for the target venue.

## What This Does

Takes the assembled paper through final formatting, verification, and packaging
to produce a submission-ready ZIP file.

## Prerequisites

Verify before starting:
- `papers/<slug>/main.tex` exists and compiles
- `papers/<slug>/references.bib` is complete
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
- Apply the correct year's style file
- Check page limits (count carefully!)
- Add/remove anonymization as appropriate
- Add acknowledgments section (camera-ready only)
- Add venue-specific checklist (NeurIPS requires this)
- Verify figure resolution

### Step 3: Final Compilation
```bash
cd papers/<slug>/camera-ready
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
- [ ] All equations are properly formatted (no overlapping symbols)
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
cd papers/<slug>/camera-ready
# Create zip with all required files
zip -r ../submission.zip main.tex references.bib *.sty *.cls figures/
```

Report: "Camera-ready package created at `papers/<slug>/submission.zip`.
Page count: [N]/[limit]. Ready for submission to [venue]."

### Step 6: Update Current Paper Status

Update `workspace/current-paper.md`:
- Mark camera-ready as complete
- Record final page count
- Note submission date

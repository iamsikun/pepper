# /set-target

Switch the active paper target (conference or journal).

## What This Does

Changes which target `/draft-paper`, `/review-paper`, and `/camera-ready` operate on.

## Instructions

1. Read `paper/state.yaml` to see available targets and current active target.

2. If the user specified a target (e.g., `/set-target journal`), validate that the target
   directory exists in `paper/`. If not, tell the user to run `/create-journal-version` first.

3. If no target was specified, show the user the available targets with their current stages
   and ask which one to activate.

4. Update `active_target` in `paper/state.yaml`.

5. Confirm: "Active target switched to `<target>` (stage: `<stage>`)."

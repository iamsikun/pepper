#!/usr/bin/env bash
# Validates the paper-writer scaffold installation and state.
# Run from the project root.

set -euo pipefail

ERRORS=0
WARNINGS=0

echo "=== Paper Writer Validation ==="
echo ""

# 1. Path lint — no banned patterns in prompt files
echo "--- Path Lint ---"
BANNED_PATTERNS=("projects/" "papers/" "workspace/" "current-paper.md" "literature/references")
PROMPT_DIRS=(".claude/agents" ".claude/commands")

for dir in "${PROMPT_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    for file in "$dir"/*.md; do
      [ -f "$file" ] || continue
      for pattern in "${BANNED_PATTERNS[@]}"; do
        if grep -q "$pattern" "$file" 2>/dev/null; then
          echo "FAIL: $file contains banned pattern '$pattern'"
          ERRORS=$((ERRORS + 1))
        fi
      done
    done
  fi
done

if [ $ERRORS -eq 0 ]; then
  echo "PASS: No banned patterns found in prompt files"
fi

# 2. Template lint — every template dir has manifest
echo ""
echo "--- Template Lint ---"
TEMPLATE_DIR=".paperwriter/templates"
if [ -d "$TEMPLATE_DIR" ]; then
  for venue_dir in "$TEMPLATE_DIR"/*/; do
    [ -d "$venue_dir" ] || continue
    venue_name=$(basename "$venue_dir")
    if [ ! -f "$venue_dir/template-manifest.yaml" ]; then
      echo "FAIL: $venue_dir missing template-manifest.yaml"
      ERRORS=$((ERRORS + 1))
    else
      echo "PASS: $venue_name has template-manifest.yaml"
    fi
    if [ ! -f "$venue_dir/main.tex" ]; then
      echo "WARN: $venue_dir missing main.tex"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
else
  echo "FAIL: $TEMPLATE_DIR directory not found"
  ERRORS=$((ERRORS + 1))
fi

# 3. State lint — if paper/ exists, check state.yaml
echo ""
echo "--- State Lint ---"
if [ -d "paper" ]; then
  if [ ! -f "paper/state.yaml" ]; then
    echo "FAIL: paper/ exists but paper/state.yaml is missing"
    ERRORS=$((ERRORS + 1))
  else
    echo "PASS: paper/state.yaml exists"
    # Check active_target field exists
    if ! grep -q "active_target:" "paper/state.yaml" 2>/dev/null; then
      echo "FAIL: paper/state.yaml missing active_target field"
      ERRORS=$((ERRORS + 1))
    fi
  fi
  if [ ! -f "paper/shared/context.md" ]; then
    echo "WARN: paper/shared/context.md missing"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  echo "SKIP: paper/ not found (not initialized yet)"
fi

# 4. Required scaffold files
echo ""
echo "--- Scaffold Lint ---"
REQUIRED_FILES=("CLAUDE.md" ".claude/settings.json" ".paperwriter/config.yaml")
for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "PASS: $file exists"
  else
    echo "FAIL: $file missing"
    ERRORS=$((ERRORS + 1))
  fi
done

# 5. Legacy directories should not exist
echo ""
echo "--- Legacy Lint ---"
LEGACY_DIRS=("templates" "literature" "papers")
for dir in "${LEGACY_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "WARN: Legacy directory '$dir/' still exists"
    WARNINGS=$((WARNINGS + 1))
  fi
done

# Summary
echo ""
echo "=== Summary ==="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
  echo "VALIDATION FAILED"
  exit 1
else
  echo "VALIDATION PASSED"
  exit 0
fi

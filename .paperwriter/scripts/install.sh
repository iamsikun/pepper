#!/usr/bin/env bash
# Usage: /path/to/paper-writer/.paperwriter/scripts/install.sh [target-repo]
#
# Copies the paper-writing scaffold into the target repo.
# Safe to re-run: updates framework files, does not touch paper/ runtime state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_ROOT="${1:-.}"

# Resolve to absolute path
TARGET_ROOT="$(cd "$TARGET_ROOT" && pwd)"

echo "Installing paper-writer scaffold..."
echo "  Source: $SOURCE_ROOT"
echo "  Target: $TARGET_ROOT"

# Copy framework assets
cp -R "$SOURCE_ROOT/.claude" "$TARGET_ROOT/.claude"
cp -R "$SOURCE_ROOT/.paperwriter" "$TARGET_ROOT/.paperwriter"
cp "$SOURCE_ROOT/CLAUDE.md" "$TARGET_ROOT/CLAUDE.md"

# Add paper/ to .gitignore if not already there
touch "$TARGET_ROOT/.gitignore"
if ! grep -q '^paper/' "$TARGET_ROOT/.gitignore" 2>/dev/null; then
  echo 'paper/' >> "$TARGET_ROOT/.gitignore"
fi

echo ""
echo "Paper-writing scaffold installed into $TARGET_ROOT"
echo "Open Claude Code in your project and run /new-paper to get started."

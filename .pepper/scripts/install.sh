#!/usr/bin/env bash

set -euo pipefail

cat <<'EOF'
This script is deprecated.

Use the package workflow instead:

  uv add --dev git+ssh://git@github.com/<you>/<pepper-private-repo>.git --tag v0.1.0
  uv run pepper install
EOF

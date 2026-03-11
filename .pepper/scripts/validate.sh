#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

PYTHONPATH="$SOURCE_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" python3 -m pepper validate "$@"

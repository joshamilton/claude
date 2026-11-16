#!/usr/bin/env bash
# Point this repository at the shared pre-commit hook in .githooks/
set -euo pipefail

chmod +x .githooks/pre-commit
git config core.hooksPath .githooks

echo "Git hooks path set to .githooks (pre-commit runs scripts/lint.sh then scripts/test.sh)."

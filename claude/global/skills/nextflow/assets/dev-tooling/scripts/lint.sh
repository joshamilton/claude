#!/usr/bin/env bash
# Run nextflow lint and nf-core lint
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "lint.sh: nextflow lint"
export NXF_SYNTAX_PARSER=v2
PATHS=(main.nf nextflow.config workflows/ subworkflows/local/ conf/)
[[ -d modules/local ]] && PATHS+=(modules/local/)
mamba run -n [project-name] \
  nextflow lint -project-dir . "${PATHS[@]}"

echo "lint.sh: nf-core pipelines lint"
mamba run -n [project-name] \
  nf-core pipelines lint --dir . --plain-text

echo "lint.sh: nf-core modules lint"
mamba run -n [project-name] \
  nf-core modules lint --dir . --local --plain-text --fail-warned

echo "lint.sh: nf-core subworkflows lint"
mamba run -n [project-name] \
  nf-core subworkflows lint --dir . --local --plain-text --fail-warned

echo "lint.sh: passed"

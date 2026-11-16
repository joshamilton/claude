#!/usr/bin/env bash
# Run nf-test component and pipeline integration tests
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

resolve_nfcore_test_dir() {
  local file="$1" dir
  dir="$(dirname "$file")"
  while [[ "$dir" != . && "$dir" != modules/nf-core && "$dir" != subworkflows/nf-core ]]; do
    if [[ -f "$dir/tests/main.nf.test" ]]; then
      printf '%s\n' "$dir/tests/"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

if git diff --cached --name-only -- modules/nf-core subworkflows/nf-core | grep -q .; then
  NFCORE_TEST_DIRS=()
  while IFS= read -r dir; do
    [[ -n "$dir" ]] || continue
    NFCORE_TEST_DIRS+=("$dir")
  done < <(
    while IFS= read -r file; do
      [[ -n "$file" ]] || continue
      resolve_nfcore_test_dir "$file" || true
    done < <(git diff --cached --name-only -- modules/nf-core subworkflows/nf-core) |
      awk '!seen[$0]++'
  )

  if ((${#NFCORE_TEST_DIRS[@]} == 0)); then
    echo "test.sh: skipping nf-core component tests (no test dirs for changed paths)"
  else
    echo "test.sh: nf-core paths changed — running ${#NFCORE_TEST_DIRS[@]} component test suite(s)"
    mamba run -n [project-name] nf-test test \
      "${NFCORE_TEST_DIRS[@]}" \
      --profile local -c nf-test.config
  fi
else
  echo "test.sh: skipping nf-core component tests (no nf-core paths in commit)"
fi

echo "test.sh: local module tests"
mamba run -n [project-name] \
  nf-test test modules/local/ --profile local -c nf-test.config

echo "test.sh: local subworkflow tests"
mamba run -n [project-name] \
  nf-test test subworkflows/local/ --profile local -c nf-test.config

echo "test.sh: pipeline integration tests"
mamba run -n [project-name] \
  nf-test test tests/default_local.nf.test --profile +local -c nf-test.config

echo "test.sh: passed"

#!/usr/bin/env bash
set -euo pipefail

# Find the latest folder in the out directory and run pytest on its tests.py
# Usage:
#   bash run_latest_tests.sh [--junitxml]
# If --junitxml is passed, a JUnit report will be written next to tests.py as report.xml

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$ROOT_DIR/out"

if [[ ! -d "$OUT_DIR" ]]; then
  echo "Error: out directory not found at $OUT_DIR" >&2
  exit 1
fi

# Determine the latest run directory by sorting folder names descending
# Folders are expected to be named like YYYYMMDD_HHMMSS
latest_folder="$(ls -1 "$OUT_DIR" 2>/dev/null | sort -r | head -n 1)"

if [[ -z "${latest_folder:-}" ]]; then
  echo "Error: No run folders found inside $OUT_DIR" >&2
  exit 1
fi

RUN_DIR="$OUT_DIR/$latest_folder"
TEST_FILE="$RUN_DIR/tests.py"

if [[ ! -f "$TEST_FILE" ]]; then
  echo "Error: tests.py not found at $TEST_FILE" >&2
  exit 1
fi

# Prefer the project's virtualenv pytest if available
if [[ -x "$ROOT_DIR/.venv/bin/pytest" ]]; then
  PYTEST_BIN="$ROOT_DIR/.venv/bin/pytest"
else
  PYTEST_BIN="pytest"
fi

# Optional JUnit XML output flag
#JUNIT_FLAG=()
#if [[ "${1:-}" == "--junitxml" ]]; then
#  JUNIT_FLAG=("--junitxml=$RUN_DIR/report.xml")
#fi

echo "Latest run directory: $RUN_DIR"
echo "Running: $PYTEST_BIN $TEST_FILE"
exec "$PYTEST_BIN" "$TEST_FILE" --maxfail=1 --disable-warnings --tb=short

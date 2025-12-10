#!/bin/bash
set -euo pipefail

echo "[compare_schemas] Comparing TEST and STAGE DB schemas..."

# === НАСТРОЙКИ ПОД СЕБЯ ===============================
# TEST-сервер
TEST_DB_HOST="${TEST_DB_HOST:-localhost}"
TEST_DB_PORT="${TEST_DB_PORT:-5432}"
TEST_DB_NAME="${TEST_DB_NAME:-library_test}"
TEST_DB_USER="${TEST_DB_USER:-postgres}"
TEST_DB_PASSWORD="${TEST_DB_PASSWORD:-password}"

# STAGE-сервер
STAGE_DB_HOST="${STAGE_DB_HOST:-localhost}"
STAGE_DB_PORT="${STAGE_DB_PORT:-5432}"
STAGE_DB_NAME="${STAGE_DB_NAME:-library_stage}"
STAGE_DB_USER="${STAGE_DB_USER:-postgres}"
STAGE_DB_PASSWORD="${STAGE_DB_PASSWORD:-password}"
# =======================================================

TMP_DIR="tmp_schema"
mkdir -p "$TMP_DIR"

TEST_SCHEMA_FILE="${TMP_DIR}/test_schema.sql"
STAGE_SCHEMA_FILE="${TMP_DIR}/stage_schema.sql"
DIFF_FILE="${TMP_DIR}/schema_diff.patch"

echo "[compare_schemas] Dumping TEST schema..."
PGPASSWORD="$TEST_DB_PASSWORD" \
pg_dump \
  -h "$TEST_DB_HOST" \
  -p "$TEST_DB_PORT" \
  -U "$TEST_DB_USER" \
  -s "$TEST_DB_NAME" > "$TEST_SCHEMA_FILE"

echo "[compare_schemas] Dumping STAGE schema..."
PGPASSWORD="$STAGE_DB_PASSWORD" \
pg_dump \
  -h "$STAGE_DB_HOST" \
  -p "$STAGE_DB_PORT" \
  -U "$STAGE_DB_USER" \
  -s "$STAGE_DB_NAME" > "$STAGE_SCHEMA_FILE"

echo "[compare_schemas] Running diff..."
if diff -u "$TEST_SCHEMA_FILE" "$STAGE_SCHEMA_FILE" > "$DIFF_FILE"; then
    echo "[compare_schemas] Schemas are IDENTICAL."
    exit 0
else
    echo "[compare_schemas] Schemas are DIFFERENT!"
    echo "[compare_schemas] Diff saved to: $DIFF_FILE"
    exit 0
fi

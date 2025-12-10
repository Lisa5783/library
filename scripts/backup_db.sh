#!/bin/bash
set -e

echo "[backup_db] Starting simulated backup..."
mkdir -p db_backups

cp db_schema/schema.sql "db_backups/backup_$(date +%Y%m%d_%H%M%S).sql"

echo "[backup_db] Backup finished."
exit 0

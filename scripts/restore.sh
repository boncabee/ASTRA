#!/usr/bin/env bash
set -eo pipefail

# ASTRA Restore Automation Script
# Usage: ./scripts/restore.sh backups/astra_backup_20260616_120000.sql.gz
#
# Format: plain SQL compressed with gzip (produced by backup.sh)
# Restore method: gunzip | psql  (NOT pg_restore — backup is plain SQL, not custom binary)

if [ -z "$1" ]; then
  echo "Error: No backup file specified."
  echo "Usage: $0 path/to/backup.sql.gz"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: Backup file '${BACKUP_FILE}' not found."
  exit 1
fi

echo "WARNING: This will overwrite the existing database!"
read -p "Are you sure you want to proceed? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Restore cancelled."
  exit 1
fi

DB_USER=${POSTGRES_USER:-postgres}
DB_NAME=${POSTGRES_DB:-astra}

echo "Restoring ASTRA database from ${BACKUP_FILE}..."

# Plain SQL + gzip: decompress then pipe into psql
gunzip -c "$BACKUP_FILE" | docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME"

echo "Restore completed successfully."


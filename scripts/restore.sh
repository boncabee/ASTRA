#!/usr/bin/env bash
set -eo pipefail

# ASTRA Restore Automation Script
# Usage: ./scripts/restore.sh backups/astra_backup_20260616_120000.sql.gz

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

# We use pg_restore since backup.sh uses custom format (-F c)
gunzip -c "$BACKUP_FILE" | docker compose exec -T db pg_restore -U "$DB_USER" -d "$DB_NAME" --clean --if-exists

if [ $? -eq 0 ]; then
  echo "Restore completed successfully."
else
  echo "Restore failed!" >&2
  exit 1
fi

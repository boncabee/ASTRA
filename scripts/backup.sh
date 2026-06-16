#!/usr/bin/env bash
set -eo pipefail

# ASTRA Backup Automation Script
# Usage: ./scripts/backup.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/astra_backup_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "Starting ASTRA database backup..."

# Extract credentials from environment or fallback to defaults
DB_USER=${POSTGRES_USER:-postgres}
DB_NAME=${POSTGRES_DB:-astra}

# Execute pg_dump inside the running db container via docker compose
docker compose exec -T db pg_dump -U "$DB_USER" -d "$DB_NAME" -F c | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Backup successfully created: ${BACKUP_FILE}"
else
  echo "Backup failed!" >&2
  exit 1
fi

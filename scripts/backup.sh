#!/usr/bin/env bash
set -eo pipefail

# ASTRA Backup Automation Script
# Usage: ./scripts/backup.sh
#
# Format: plain SQL piped through gzip (.sql.gz)
# Restore: gunzip -c <file> | docker compose exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB
# Note: do NOT use -F c (custom binary) with gzip — they are incompatible.

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/astra_backup_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "Starting ASTRA database backup..."

# Extract credentials from environment or fallback to defaults
DB_USER=${POSTGRES_USER:-postgres}
DB_NAME=${POSTGRES_DB:-astra}

# Plain SQL format (-F p is default) piped through gzip — readable by gunzip | psql
docker compose exec -T db pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_FILE"

echo "Backup successfully created: ${BACKUP_FILE}"

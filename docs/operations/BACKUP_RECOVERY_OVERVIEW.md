# Backup & Recovery Overview

## Strategy
ASTRA treats the PostgreSQL database as the sole source of state. Because ASTRA is a system of record with immutable evidence, strict backup strategies are required to meet Recovery Point Objectives (RPO) and Recovery Time Objectives (RTO).

## Backup Process
- **Mechanism:** Backups are currently performed via logical SQL dumps (`pg_dump`) compressed with gzip.
- **Cadence:** Backups execute automatically via a cron job on the host machine.
- **Offsite Sync:** To protect against node failure, the encrypted backup archives must be synchronized to an offsite storage bucket (e.g., AWS S3 or Google Cloud Storage) immediately after creation.

## Recovery Process
In the event of catastrophic data corruption or node failure:
1. Provision a clean host and deploy the ASTRA stack.
2. Stop the application container (`docker-compose stop backend`) to prevent writes.
3. Drop the corrupted database schema and recreate it.
4. Execute `gunzip -c backup.sql.gz | psql -U astra` to restore the state.
5. Restart the application and verify health metrics.

## Disaster Recovery Drills
Operators must conduct quarterly "Game Days" involving a full restoration to a sterile staging environment to validate the integrity of the backup chain and verify the RTO.

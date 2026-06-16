# ASTRA Backup & Restore Runbook

**Document ID:** ASTRA-OPS-001  
**Version:** 1.0  
**Status:** Approved  

## Purpose
This runbook defines the standard operating procedures for executing manual or automated backups of the ASTRA PostgreSQL database, and details the steps required to restore the application to a known good state.

## Backup Methodology
ASTRA uses `pg_dump` via logical backup, streamed directly from the `db` container into a compressed `.sql.gz` archive on the host filesystem. This prevents the need for intermediate container storage and simplifies host-level offsite replication.

The backup includes the complete database schema, user data, policy configurations, and the immutable audit logs.

### Executing a Backup

To execute a backup manually, run the provided automation script from the repository root:

```bash
./scripts/backup.sh
```

**Expected Output:**
```text
Starting ASTRA database backup...
Backup successfully created: backups/astra_backup_20260616_120000.sql.gz
```

### Automated Backups (Cron Integration)
For Small Team deployments, it is recommended to schedule `backup.sh` via a host-level cron job.

```cron
# Execute daily at 02:00 AM system time
0 2 * * * cd /path/to/astra && ./scripts/backup.sh >> /var/log/astra_backup.log 2>&1
```

## Restore Methodology
Restoring the database utilizes `pg_restore`. The script is designed to accept the compressed backup file, stream it to the container, and automatically drop and recreate the necessary schema objects to ensure a clean state (`--clean --if-exists`).

### Executing a Restore

> [!WARNING]
> Restoring a database is a destructive action that will overwrite the current live database state. All data created after the backup timestamp will be permanently lost.

To execute a restore, provide the target backup file as an argument:

```bash
./scripts/restore.sh backups/astra_backup_20260616_120000.sql.gz
```

**Expected Output:**
```text
WARNING: This will overwrite the existing database!
Are you sure you want to proceed? (y/N) y
Restoring ASTRA database from backups/astra_backup_20260616_120000.sql.gz...
Restore completed successfully.
```

## Verification
Following a successful restore, operators must verify the application state:
1. Navigate to the ASTRA web interface.
2. Ensure authentication works.
3. Validate that the Case Timeline and Policy configurations reflect the time of the backup.
4. Check `docker compose logs backend` for any unexpected database connection errors.

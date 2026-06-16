# ASTRA Disaster Recovery Runbook

**Document ID:** ASTRA-OPS-002  
**Version:** 1.0  
**Status:** Approved  

## Purpose
This document provides prescriptive guidance for recovering the ASTRA platform from catastrophic failures, including hardware loss, logical data corruption, and accidental data deletion.

## RPO & RTO Definitions

The ASTRA architecture is designed to support the following business continuity targets based on the deployment scale:

### Single-Node Deployment (Sandbox / Local)
- **Recovery Point Objective (RPO):** 24 hours (assumes daily manual or automated cron backup).
- **Recovery Time Objective (RTO):** 2 hours.
- **Strategy:** Local host-bound backups stored in the `backups/` directory.

### Small Team Deployment (Production Pilot)
- **Recovery Point Objective (RPO):** 1-4 hours (requires frequent automated backups and off-host syncing).
- **Recovery Time Objective (RTO):** 4 hours (accounts for time required to provision a new virtual machine and pull images).
- **Strategy:** Compressed backups automatically synced to S3/Blob storage immediately after creation.

## Disaster Scenarios

### Scenario 1: Accidental Deletion / Data Corruption
**Symptom:** A user accidentally deletes a critical Policy, or a bug corrupts Case Evidence links.
**Response:**
1. Determine the timestamp of the corruption event.
2. Isolate the environment by stopping the backend container: `docker compose stop backend`
3. Identify the most recent backup file prior to the event.
4. Execute the restore: `./scripts/restore.sh path/to/backup.sql.gz`
5. Restart the backend container: `docker compose start backend`
6. Verify data integrity.

### Scenario 2: Container Loss (Docker Engine Failure)
**Symptom:** The `db` or `backend` container refuses to start, or Docker volumes are wiped.
**Response:**
1. Verify if the Docker volumes (`db_data`) still exist. If yes, simply run `docker compose up -d` to recreate containers attached to the existing state.
2. If volumes were destroyed (e.g., `docker compose down -v`), you must perform a full restore.
3. Bring up a fresh database container: `docker compose up -d db`
4. Wait for PostgreSQL to initialize (check `docker compose logs db`).
5. Execute the restore script with the latest backup.
6. Bring up the remaining stack: `docker compose up -d`

### Scenario 3: Complete Host Loss
**Symptom:** The virtual machine or physical server running ASTRA is destroyed or permanently inaccessible.
**Response:**
1. Provision a new host environment following `LOCAL_DEVELOPMENT_SETUP.md` or `DEPLOYMENT.md` guidelines.
2. Clone the ASTRA repository to the new host.
3. Retrieve the latest off-site backup file from cloud storage (S3/Blob).
4. Configure the `.env` file with the identical secrets (specifically `JWT_SECRET_KEY`) used on the old host to ensure existing user sessions or tokens remain valid if necessary.
5. Launch the database: `docker compose up -d db`
6. Execute the restore script.
7. Launch the full application stack.
8. Re-point DNS or load balancers to the new host IP.

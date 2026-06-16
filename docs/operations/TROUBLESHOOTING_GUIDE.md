# Troubleshooting Guide

## Purpose
This document catalogs common issues, root causes, and resolutions discovered during the ASTRA local environment validation and stabilization efforts. It serves as the first line of defense for developer friction.

## Scope
This guide addresses configuration, connectivity, testing, and environment setup issues for the ASTRA backend application.

## Issues and Resolutions

### 1. Missing `.env`
- **Symptoms:** Application fails to start, throwing `ValidationError` for missing configuration variables like `DATABASE_URL`.
- **Root Cause:** The developer cloned the repository but did not create the local `.env` file.
- **Resolution:** Copy the example configuration file: `cp .env.example .env` (ensure it is placed in the required directory, usually `backend/`).
- **Prevention:** Document the `.env` setup prominently in the Local Development Setup guide.

### 2. Incorrect `DATABASE_URL`
- **Symptoms:** Application startup crashes with `asyncpg.exceptions.InvalidPasswordError` or connection timeouts.
- **Root Cause:** The `DATABASE_URL` contains the wrong password, wrong driver (e.g., missing `+asyncpg`), or wrong port.
- **Resolution:** Update `DATABASE_URL` in the `.env` file to match the Docker configuration: `postgresql+asyncpg://postgres:postgres@localhost:5432/astra`.
- **Prevention:** Standardize the local `docker-compose.yml` credentials and provide exact copy-paste strings in the docs.

### 3. Incorrect `TEST_DATABASE_URL`
- **Symptoms:** Tests fail immediately with database connection errors, while the application runs fine.
- **Root Cause:** `TEST_DATABASE_URL` is pointing to the wrong database or is entirely missing from the environment.
- **Resolution:** Set `TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/astra_test` in the `backend/.env` file.
- **Prevention:** Add connection string checks at the start of the pytest `conftest.py` setup.

### 4. Missing `astra_test` Database
- **Symptoms:** Pytest fails with `asyncpg.exceptions.InvalidCatalogNameError: database "astra_test" does not exist`.
- **Root Cause:** The Docker initialization script (`init.sql`) failed to run, or the volume was created before the script was added.
- **Resolution:** Tear down the database volume and restart: `docker-compose down -v && docker-compose up -d db`.
- **Prevention:** Ensure `docker-entrypoint-initdb.d` scripts are properly configured and documented in the PostgreSQL guide.

### 5. Alembic Connectivity Failures
- **Symptoms:** `alembic upgrade head` hangs or throws a `ConnectionRefusedError`.
- **Root Cause:** Alembic is trying to connect to a database that isn't running, or it's utilizing a synchronous URL when an async URL is provided (or vice versa, depending on `env.py` setup).
- **Resolution:** Ensure the Docker container is running (`docker ps`). Verify `alembic.ini` and `env.py` are properly configured to ingest the URL from the environment.
- **Prevention:** Standardize the `env.py` loading mechanism across the team.

### 6. Interpreter Resolution Issues
- **Symptoms:** Terminal throws `ModuleNotFoundError` for packages that are clearly in `requirements.txt`.
- **Root Cause:** The global Python interpreter is being used instead of the virtual environment interpreter.
- **Resolution:** Activate the virtual environment: `source venv/bin/activate` (Linux/Mac/WSL) or `.\venv\Scripts\activate` (Windows).
- **Prevention:** Always document `source venv/bin/activate` as a required step before running commands.

### 7. VS Code / Antigravity Interpreter Issues
- **Symptoms:** IDE shows import errors (red squiggles) despite the application running correctly in the terminal.
- **Root Cause:** VS Code is pointing to the system Python interpreter instead of the workspace virtual environment.
- **Resolution:** Open the Command Palette (`Ctrl+Shift+P`), select `Python: Select Interpreter`, and choose the interpreter path inside your `./venv/` (or `backend/venv/`) directory.
- **Prevention:** Include a `.vscode/settings.json` file in the repository with `"python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python"`.

### 8. pytest Collection Failures
- **Symptoms:** Running `pytest` results in `ERROR: file or directory not found` or `ModuleNotFoundError` during the collection phase.
- **Root Cause:** `pytest` is executed from the repository root, confusing Python's `sys.path` and module resolution.
- **Resolution:** Navigate to the `backend/` directory before executing the command: `cd backend/ && pytest`.
- **Prevention:** Explicitly state the required working directory in the Testing Guide.

### 9. Wrong Execution Directory
- **Symptoms:** Alembic reports `No such file or directory: alembic.ini`, or Uvicorn fails to find `app.main:app`.
- **Root Cause:** The developer is running commands from the repository root instead of the `backend/` directory.
- **Resolution:** Execute all backend-specific commands (alembic, uvicorn, pytest, mypy) from within the `backend/` directory.
- **Prevention:** Bold and highlight working directory requirements in all procedural documentation.

## Verification
- If an issue is resolved using this guide, verify functionality by running the full test suite (`pytest`) from the `backend/` directory.

## References
- [Local Development Setup Guide](./LOCAL_DEVELOPMENT_SETUP.md)
- [Testing Guide](./TESTING_GUIDE.md)

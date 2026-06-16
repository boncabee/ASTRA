# Local Development Setup Guide

## Purpose
This document provides a comprehensive, step-by-step guide for setting up the ASTRA local development environment. It is designed to prevent repetitive debugging of environment configuration and ensure a standardized setup across the team.

## Scope
This guide covers the setup of the backend application, PostgreSQL database via Docker, frontend application (if applicable), and all necessary system prerequisites on a Windows machine utilizing WSL2.

## Procedure

### 1. Prerequisites
Ensure you have administrative access to your Windows machine to install necessary tools.

### 2. Windows and WSL2 Setup
1. Open PowerShell as Administrator.
2. Run the command to install WSL2: `wsl --install`
3. Restart your machine if prompted.
4. Set WSL2 as your default version: `wsl --set-default-version 2`
5. Install your preferred Linux distribution (e.g., Ubuntu) from the Microsoft Store.

### 3. Docker Desktop Setup
1. Download and install Docker Desktop for Windows.
2. During installation, ensure the **"Use WSL 2 instead of Hyper-V"** option is checked.
3. Once installed, go to Docker Desktop Settings > Resources > WSL Integration.
4. Enable integration for your installed Linux distribution.
5. Restart Docker Desktop.

### 4. Python Installation
1. Open your WSL terminal (e.g., Ubuntu).
2. Update packages: `sudo apt update && sudo apt upgrade -y`
3. Install Python 3.10+ (if not already present): `sudo apt install python3.10 python3.10-venv python3-pip -y`

### 5. Virtual Environment Setup
1. Navigate to the project root directory in your WSL terminal.
2. Create the virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r backend/requirements.txt` (or equivalent dependency command).

### 6. Environment Variables
1. Copy the example `.env` file in the root and `backend/` directory (if applicable): `cp .env.example .env`
2. Ensure the following database configurations are correctly set in the `backend/.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/astra
   TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/astra_test
   ```

### 7. PostgreSQL Container Startup
1. Ensure Docker Desktop is running.
2. Navigate to the directory containing the `docker-compose.yml` file.
3. Start the database containers: `docker-compose up -d db`
4. Verify containers are running: `docker ps`

### 8. Alembic Migration Workflow
1. Navigate to the `backend/` directory: `cd backend/`
2. Run all database migrations to initialize the schema: `alembic upgrade head`
3. Verify successful migration output indicating the schema is up to date.

### 9. Backend Startup
1. Remain in the `backend/` directory.
2. Start the FastAPI backend server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
3. The API will be accessible at `http://localhost:8000`.

### 10. Frontend Startup
*(If a frontend application is currently integrated)*
1. Open a new WSL terminal and navigate to the `frontend/` directory.
2. Install Node dependencies: `npm install`
3. Start the frontend development server: `npm run dev`

## Verification
### Verification Checklist
- [ ] WSL2 is installed and functional.
- [ ] Docker Desktop is running with WSL2 integration enabled.
- [ ] Python virtual environment is activated.
- [ ] PostgreSQL Docker container is running and accessible.
- [ ] `alembic upgrade head` completes without errors.
- [ ] Backend server starts successfully on port 8000.
- [ ] Swagger API docs are accessible at `http://localhost:8000/docs`.

## Troubleshooting
Refer to the [Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md) for issues related to missing `.env` files, PostgreSQL connection errors, and Alembic failures.

## References
- [Docker Documentation](https://docs.docker.com/)
- [WSL2 Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [PostgreSQL Development Guide](./POSTGRESQL_DEVELOPMENT_GUIDE.md)

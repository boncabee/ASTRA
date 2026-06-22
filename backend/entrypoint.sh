#!/bin/bash
set -e

echo "Waiting for database..."
TIMEOUT=60
ELAPSED=0
until alembic current > /dev/null 2>&1; do
  if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
    echo "ERROR: Database did not become available within ${TIMEOUT} seconds."
    echo "Check DATABASE_URL in .env and ensure the 'db' service is healthy."
    exit 1
  fi
  echo "Database not ready yet, waiting 1 second... (${ELAPSED}s elapsed)"
  sleep 1
  ELAPSED=$((ELAPSED + 1))
done

echo "Database ready. Running migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"

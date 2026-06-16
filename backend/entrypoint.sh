#!/bin/bash
set -e

echo "Waiting for database..."
while ! alembic current > /dev/null 2>&1; do
  echo "Database not ready yet, waiting 1 second..."
  sleep 1
done

echo "Database ready. Running migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"

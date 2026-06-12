#!/bin/bash
echo "Rolling back ASTRA deployment..."
docker compose -f docker-compose.yml down
echo "Rollback initiated. Services stopped."

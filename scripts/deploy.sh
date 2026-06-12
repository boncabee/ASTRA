#!/bin/bash
echo "Deploying ASTRA to staging environment..."
docker compose -f docker-compose.yml up -d
echo "Deployment initiated."

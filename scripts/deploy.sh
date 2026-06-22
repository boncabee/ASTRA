#!/bin/bash
set -eo pipefail

# ==============================================================================
# ASTRA Production Deployment Script
# ==============================================================================
# This script deploys the ASTRA production stack using docker-compose.prod.yml.
# It MUST NOT be used for local development (use docker-compose.yml instead).
#
# Usage: ./scripts/deploy.sh
# ==============================================================================

# Safety guard: confirm production context
echo "============================================="
echo "  ASTRA Production Deployment"
echo "============================================="
echo ""
echo "This will deploy using docker-compose.prod.yml against a PRODUCTION environment."
echo "Ensure .env is populated with secure, production-grade values."
echo ""
read -r -p "Are you sure you want to deploy to PRODUCTION? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
  echo "Deployment cancelled."
  exit 0
fi

# Verify .env exists
if [ ! -f .env ]; then
  echo "ERROR: .env file not found. Copy .env.example to .env and populate all values."
  exit 1
fi

# Verify ENVIRONMENT is set to prod
ENV_VALUE=$(grep -E '^ENVIRONMENT=' .env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d '"')
if [ "$ENV_VALUE" != "prod" ]; then
  echo "ERROR: ENVIRONMENT in .env is not set to 'prod' (current: '${ENV_VALUE}')."
  echo "Production deployments require ENVIRONMENT=prod to activate security guards."
  exit 1
fi

echo ""
echo "Deploying ASTRA production stack..."
docker compose -f docker-compose.prod.yml up -d --build

echo ""
echo "Deployment initiated. Checking status..."
sleep 5
docker compose -f docker-compose.prod.yml ps

echo ""
echo "To verify health: curl -k https://\${DOMAIN}/api/v1/health"
echo "To view logs:     docker compose -f docker-compose.prod.yml logs -f"

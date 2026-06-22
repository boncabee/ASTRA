#!/bin/bash
# ==============================================================================
# ASTRA Staging Deployment Script
# ==============================================================================
# Deploys the ASTRA staging stack using docker-compose.prod.yml with the
# staging .env.staging file. Staging runs on the same stack configuration
# as production but with isolated secrets and a separate database.
#
# Usage: ./scripts/deploy-staging.sh
# ==============================================================================

set -eo pipefail

echo "============================================="
echo "  ASTRA Staging Deployment"
echo "============================================="
echo ""

# Verify .env.staging exists
if [ ! -f .env.staging ]; then
  echo "ERROR: .env.staging not found."
  echo "Copy .env.example to .env.staging and populate staging-specific values."
  exit 1
fi

# Verify ENVIRONMENT is prod (staging uses same guard)
ENV_VALUE=$(grep -E '^ENVIRONMENT=' .env.staging | cut -d '=' -f2 | tr -d '[:space:]' | tr -d '"')
if [ "$ENV_VALUE" != "prod" ]; then
  echo "ERROR: ENVIRONMENT in .env.staging must be 'prod' to activate security guards."
  exit 1
fi

echo "Deploying ASTRA staging stack..."
docker compose --env-file .env.staging -f docker-compose.prod.yml up -d --build

echo ""
echo "Staging deployment initiated."
STAGING_DOMAIN=$(grep -E '^DOMAIN=' .env.staging | cut -d '=' -f2)
echo "Health: https://${STAGING_DOMAIN}/api/v1/health"
echo "Logs:   docker compose --env-file .env.staging -f docker-compose.prod.yml logs -f"

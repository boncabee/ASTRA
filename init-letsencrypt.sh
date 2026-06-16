#!/bin/bash
set -e

# ==============================================================================
# ASTRA TLS Bootstrap Automation Script
# ==============================================================================
# This script automates the initial generation of Let's Encrypt certificates.
# It resolves the NGINX SSL "chicken-and-egg" failure by generating a temporary
# self-signed dummy certificate, allowing NGINX to boot and process the actual
# Certbot ACME webroot challenge, and then cleanly swapping to the valid cert.
# ==============================================================================

if [ ! -f .env ]; then
  echo "Error: .env file not found. Please copy .env.example to .env and configure it."
  exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

if [ -z "$DOMAIN" ] || [ "$DOMAIN" == "example.com" ]; then
  echo "Error: DOMAIN must be set to a valid domain in .env (current: $DOMAIN)"
  exit 1
fi

echo "==========================================================="
echo "Bootstrapping Let's Encrypt TLS for $DOMAIN"
echo "==========================================================="

RSA_KEY_SIZE=4096

echo "### Checking for existing certificates..."
if docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  sh -c 'test -d /etc/letsencrypt/live/$DOMAIN'" certbot > /dev/null 2>&1; then
  echo "Existing certificate found for $DOMAIN. Exiting."
  exit 0
fi

echo "### Creating dummy certificate for $DOMAIN ..."
docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  sh -c 'mkdir -p /etc/letsencrypt/live/$DOMAIN && \
  openssl req -x509 -nodes -newkey rsa:$RSA_KEY_SIZE -days 1 \
    -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
    -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
    -subj \"/CN=localhost\"'" certbot

echo "### Starting NGINX ..."
docker compose -f docker-compose.prod.yml up -d proxy

echo "### Deleting dummy certificate for $DOMAIN ..."
docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$DOMAIN && \
  rm -Rf /etc/letsencrypt/archive/$DOMAIN && \
  rm -Rf /etc/letsencrypt/renewal/$DOMAIN.conf" certbot

echo "### Requesting Let's Encrypt certificate for $DOMAIN ..."
# Use an email parameter if provided, otherwise register without email.
EMAIL_ARG="--register-unsafely-without-email"
if [ ! -z "$CERTBOT_EMAIL" ]; then
    EMAIL_ARG="--email $CERTBOT_EMAIL"
fi

docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $EMAIL_ARG \
    -d $DOMAIN \
    --rsa-key-size $RSA_KEY_SIZE \
    --agree-tos \
    --force-renewal" certbot

echo "### Reloading NGINX ..."
docker compose -f docker-compose.prod.yml exec proxy nginx -s reload

echo "==========================================================="
echo "TLS Bootstrap Complete!"
echo "==========================================================="

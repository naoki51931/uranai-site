#!/usr/bin/env bash
set -eu

COMPOSE_FILES="-f docker-compose.yml -f docker-compose-free.yml"

if [ -z "${LETSENCRYPT_EMAIL:-}" ] || [ -z "${LETSENCRYPT_PRIMARY_DOMAIN:-}" ] || [ -z "${LETSENCRYPT_DOMAINS:-}" ]; then
  echo "LETSENCRYPT_EMAIL, LETSENCRYPT_PRIMARY_DOMAIN, and LETSENCRYPT_DOMAINS are required."
  exit 1
fi

domain_args=""
for domain in ${LETSENCRYPT_DOMAINS}; do
  domain_args="$domain_args -d $domain"
done

sudo docker compose --env-file .env ${COMPOSE_FILES} run --rm certbot certonly \
  --webroot \
  --webroot-path /var/www/certbot \
  --email "${LETSENCRYPT_EMAIL}" \
  --agree-tos \
  --no-eff-email \
  ${domain_args}

sudo docker compose --env-file .env ${COMPOSE_FILES} restart nginx

#!/usr/bin/env bash
set -eu

COMPOSE_FILES="-f docker-compose.yml -f docker-compose-free.yml"

sudo docker compose --env-file .env ${COMPOSE_FILES} run --rm certbot renew --webroot --webroot-path /var/www/certbot --no-random-sleep-on-renew
sudo docker compose --env-file .env ${COMPOSE_FILES} restart nginx

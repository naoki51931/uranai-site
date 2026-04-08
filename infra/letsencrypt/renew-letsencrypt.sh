#!/usr/bin/env bash
set -eu

sudo docker compose run --rm certbot renew --webroot --webroot-path /var/www/certbot
sudo docker compose restart nginx

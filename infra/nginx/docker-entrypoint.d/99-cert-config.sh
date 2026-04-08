#!/bin/sh
set -eu

HTTPS_TEMPLATE="/etc/nginx/templates/https.conf.template"
HTTP_TEMPLATE="/etc/nginx/templates/http-only.conf.template"
ACTIVE_CONFIG="/etc/nginx/conf.d/default.conf"
CERT_DIR="/etc/letsencrypt/live/${LETSENCRYPT_PRIMARY_DOMAIN:-}"

if [ -n "${LETSENCRYPT_PRIMARY_DOMAIN:-}" ] && [ -f "${CERT_DIR}/fullchain.pem" ] && [ -f "${CERT_DIR}/privkey.pem" ]; then
  envsubst '${SERVER_NAME} ${LETSENCRYPT_PRIMARY_DOMAIN}' < "${HTTPS_TEMPLATE}" > "${ACTIVE_CONFIG}"
else
  envsubst '${SERVER_NAME} ${LETSENCRYPT_PRIMARY_DOMAIN}' < "${HTTP_TEMPLATE}" > "${ACTIVE_CONFIG}"
fi

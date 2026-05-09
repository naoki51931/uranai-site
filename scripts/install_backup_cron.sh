#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$PROJECT_DIR/.env}"
CRON_TAG="# uranai-site-ai mysql backup"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/backup.log"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "env file not found: $ENV_FILE" >&2
  exit 1
fi

get_env_value() {
  local key="$1"
  local line
  line="$(grep -m1 "^${key}=" "$ENV_FILE" || true)"
  printf '%s' "${line#*=}"
}

BACKUP_CRON_SCHEDULE="${BACKUP_CRON_SCHEDULE:-$(get_env_value BACKUP_CRON_SCHEDULE)}"
BACKUP_CRON_SCHEDULE="${BACKUP_CRON_SCHEDULE:-0 2 * * *}"
BACKUP_SCRIPT="$PROJECT_DIR/scripts/backup_mysql_to_s3.sh"
CRON_LINE="$BACKUP_CRON_SCHEDULE $BACKUP_SCRIPT >> $LOG_FILE 2>&1 $CRON_TAG"

mkdir -p "$LOG_DIR"

CURRENT_CRONTAB="$(crontab -l 2>/dev/null || true)"

if grep -Fq "$CRON_TAG" <<<"$CURRENT_CRONTAB"; then
  printf '%s\n' "$CURRENT_CRONTAB" | grep -Fv "$CRON_TAG" | crontab -
fi

{
  printf '%s\n' "$CURRENT_CRONTAB" | grep -Fv "$CRON_TAG" || true
  printf '%s\n' "$CRON_LINE"
} | crontab -

echo "cron installed: $CRON_LINE"

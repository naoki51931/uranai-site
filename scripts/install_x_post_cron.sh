#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$PROJECT_DIR/.env}"
CRON_BEGIN_TAG="# uranai-site-ai daily x tarot post begin"
CRON_END_TAG="# uranai-site-ai daily x tarot post end"
CRON_TAG="# uranai-site-ai daily x tarot post"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/x-post.log"

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

X_POST_CRON_SCHEDULE="${X_POST_CRON_SCHEDULE:-$(get_env_value X_POST_CRON_SCHEDULE)}"
X_POST_CRON_SCHEDULE="${X_POST_CRON_SCHEDULE:-0 0 * * *}"
X_POST_CRON_TZ="${X_POST_CRON_TZ:-$(get_env_value X_POST_CRON_TZ)}"
X_POST_CRON_TZ="${X_POST_CRON_TZ:-Asia/Tokyo}"
POST_SCRIPT="$PROJECT_DIR/scripts/post_daily_tarot_to_x.py"
CRON_LINE="$X_POST_CRON_SCHEDULE $POST_SCRIPT --env-file $ENV_FILE >> $LOG_FILE 2>&1 $CRON_TAG"

mkdir -p "$LOG_DIR"

CURRENT_CRONTAB="$(crontab -l 2>/dev/null || true)"
FILTERED_CRONTAB="$(
  printf '%s\n' "$CURRENT_CRONTAB" \
    | sed "/^$CRON_BEGIN_TAG$/,/^$CRON_END_TAG$/d" \
    | grep -Fv "$CRON_TAG" \
    || true
)"

{
  printf '%s\n' "$FILTERED_CRONTAB" | sed '/^$/d' || true
  printf '%s\n' "$CRON_BEGIN_TAG"
  printf 'CRON_TZ=%s\n' "$X_POST_CRON_TZ"
  printf '%s\n' "$CRON_LINE"
  printf '%s\n' "$CRON_END_TAG"
} | crontab -

echo "cron installed: CRON_TZ=$X_POST_CRON_TZ $CRON_LINE"

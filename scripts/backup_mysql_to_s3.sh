#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$PROJECT_DIR/.env}"

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

MYSQL_DATABASE="${MYSQL_DATABASE:-$(get_env_value MYSQL_DATABASE)}"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-$(get_env_value MYSQL_ROOT_PASSWORD)}"
BACKUP_S3_BUCKET="${BACKUP_S3_BUCKET:-$(get_env_value BACKUP_S3_BUCKET)}"
BACKUP_S3_PREFIX="${BACKUP_S3_PREFIX:-$(get_env_value BACKUP_S3_PREFIX)}"
BACKUP_LOCAL_DIR="${BACKUP_LOCAL_DIR:-$(get_env_value BACKUP_LOCAL_DIR)}"
BACKUP_LOCAL_RETENTION_DAYS="${BACKUP_LOCAL_RETENTION_DAYS:-$(get_env_value BACKUP_LOCAL_RETENTION_DAYS)}"

required_vars=(
  MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD
  BACKUP_S3_BUCKET
)

for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "required env var is empty: $var_name" >&2
    exit 1
  fi
done

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI is not installed" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed" >&2
  exit 1
fi

DOCKER_BIN=(docker)
if ! docker version >/dev/null 2>&1; then
  if command -v sudo >/dev/null 2>&1; then
    DOCKER_BIN=(sudo docker)
  else
    echo "docker requires elevated privileges and sudo is unavailable" >&2
    exit 1
  fi
fi

BACKUP_LOCAL_DIR="${BACKUP_LOCAL_DIR:-/home/ubuntu/db-backups/uranai-site-ai}"
BACKUP_S3_PREFIX="${BACKUP_S3_PREFIX:-uranai-site-ai/mysql}"
BACKUP_LOCAL_RETENTION_DAYS="${BACKUP_LOCAL_RETENTION_DAYS:-7}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
FILE_NAME="mysql_${TIMESTAMP}.sql.gz"
TMP_FILE="$BACKUP_LOCAL_DIR/.${FILE_NAME}.tmp"
FINAL_FILE="$BACKUP_LOCAL_DIR/$FILE_NAME"
S3_URI="s3://${BACKUP_S3_BUCKET%/}/${BACKUP_S3_PREFIX#/}/$FILE_NAME"

mkdir -p "$BACKUP_LOCAL_DIR"

cd "$PROJECT_DIR"

# Dump from the running mysql container without allocating a TTY so cron can call it.
"${DOCKER_BIN[@]}" compose --env-file "$ENV_FILE" exec -T mysql \
  env MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" MYSQL_DATABASE="$MYSQL_DATABASE" \
  sh -c 'exec mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --single-transaction --quick --routines --triggers "$MYSQL_DATABASE"' \
  | gzip -c > "$TMP_FILE"

mv "$TMP_FILE" "$FINAL_FILE"

aws s3 cp --only-show-errors "$FINAL_FILE" "$S3_URI"

find "$BACKUP_LOCAL_DIR" -type f -name 'mysql_*.sql.gz' -mtime +"$BACKUP_LOCAL_RETENTION_DAYS" -delete

echo "backup uploaded: $S3_URI"

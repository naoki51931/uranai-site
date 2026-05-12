#!/bin/sh
set -eu

BLOCKLIST_CONFIG="/etc/nginx/conf.d/blocked-ips.conf"

cat > "${BLOCKLIST_CONFIG}" <<'EOF'
# Generated at container startup from BLOCKED_IPS.
EOF

if [ -z "${BLOCKED_IPS:-}" ]; then
  exit 0
fi

OLD_IFS=${IFS}
IFS=', '
set -f
for ip in ${BLOCKED_IPS}; do
  case "${ip}" in
    "" )
      continue
      ;;
    *[!0-9a-fA-F:./]* )
      echo "Skipping invalid BLOCKED_IPS entry: ${ip}" >&2
      ;;
    * )
      printf 'deny %s;\n' "${ip}" >> "${BLOCKLIST_CONFIG}"
      ;;
  esac
done
set +f
IFS=${OLD_IFS}

printf '%s\n' 'allow all;' >> "${BLOCKLIST_CONFIG}"

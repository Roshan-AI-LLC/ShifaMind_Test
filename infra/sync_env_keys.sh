#!/usr/bin/env bash
# Copy specific keys from the local .env into the box's .env, in place.
#
# The box's .env is NOT a copy of the laptop's: it holds production-only values
# (a working OPENROUTER_API_KEY, for one) that must survive. So this edits only
# the named keys and leaves every other line untouched. It never prints a value.
#
# The payload travels as a base64 ARGUMENT, not on stdin. stdin is already the
# remote script (`bash -s` reads it from there); using it for both means `cat`
# eats the rest of the script and the run dies silently, halfway, having
# written nothing.
#
# Usage, from the repo root:
#   export EC2_HOST=… EC2_USER=ubuntu SSH_KEY="…"
#   ./infra/sync_env_keys.sh SUPABASE_URL SUPABASE_SERVICE_ROLE_KEY …

set -euo pipefail

EC2_HOST="${EC2_HOST:?Set EC2_HOST}"
EC2_USER="${EC2_USER:-ubuntu}"
SSH_KEY="${SSH_KEY:?Set SSH_KEY}"
REMOTE_ENV="${REMOTE_ENV:-/home/ubuntu/shifamind/.env}"
[ "$#" -gt 0 ] || { echo "give at least one key name"; exit 2; }

payload=""
for k in "$@"; do
  line=$(grep -m1 "^$k=" .env || true)
  [ -n "$line" ] || { echo "!! $k not found in local .env"; exit 1; }
  payload+="$line"$'\n'
  echo "   will set $k"
done

# tr -d '\n': macOS base64 wraps its output, and the wrapped form does not
# survive being passed as a single shell word.
b64=$(printf '%s' "$payload" | base64 | tr -d '\n')

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new \
  "$EC2_USER@$EC2_HOST" \
  "REMOTE_ENV='$REMOTE_ENV' PAYLOAD_B64='$b64' bash -s" <<'REMOTE'
set -euo pipefail
new=$(printf '%s' "$PAYLOAD_B64" | base64 -d)
[ -n "$new" ] || { echo "!! empty payload, refusing to touch $REMOTE_ENV"; exit 1; }

cp "$REMOTE_ENV" "$REMOTE_ENV.bak.$(date +%Y%m%d%H%M%S)"
tmp=$(mktemp)
keys=$(printf '%s\n' "$new" | sed -E 's/=.*//')
while IFS= read -r line; do
  k=$(printf '%s' "$line" | sed -E 's/=.*//')
  printf '%s\n' "$keys" | grep -qx -- "$k" && continue
  printf '%s\n' "$line"
done < "$REMOTE_ENV" > "$tmp"
printf '%s\n' "$new" >> "$tmp"
mv "$tmp" "$REMOTE_ENV"
chmod 600 "$REMOTE_ENV"

echo "updated $REMOTE_ENV (backup alongside it)"
for k in $keys; do
  printf '   %s=%.24s…\n' "$k" "$(grep -m1 "^$k=" "$REMOTE_ENV" | cut -d= -f2-)"
done

cat <<'NOTE'

  The running container still holds the OLD environment: --env-file is read at
  container CREATION, and `docker restart` reuses it. Recreate:

    docker stop shifamind-api && docker rm shifamind-api
    docker run -d --name shifamind-api --restart unless-stopped -p 8000:8000 \
      -v /var/lib/shifamind/fullcode:/var/lib/shifamind/fullcode \
      --env-file /home/ubuntu/shifamind/.env shifamind-api:latest

NOTE
REMOTE

#!/usr/bin/env bash
# Build the backend image ON the EC2 box, then restart the service there.
#
# Why not infra/deploy.sh: that builds locally and ships a ~2GB tarball. The
# dev Mac is arm64 and the box is x86_64, so a local build must be emulated
# through QEMU — a torch install that way takes far longer than the native
# build on the box's own 4 vCPU, and then still has to be uploaded. Only the
# backend source is needed for the image, and that is small, so sending the
# source and building in place is faster on both counts.
#
# The previous image is tagged before it is replaced, so a rollback is one
# command. See FULLCODE_DEPLOY.md Phase 5.
#
# Usage, from the repo root:
#   export EC2_HOST=52.20.157.176 EC2_USER=ubuntu
#   export SSH_KEY="/path/with spaces/shifamind-key.pem"
#   ./infra/deploy_remote_build.sh

set -euo pipefail

EC2_HOST="${EC2_HOST:?Set EC2_HOST}"
EC2_USER="${EC2_USER:-ubuntu}"
SSH_KEY="${SSH_KEY:?Set SSH_KEY}"
REMOTE_DIR="${REMOTE_DIR:-/home/ubuntu/shifamind}"
APP="shifamind-api"

# Quoted so a key path containing spaces survives. rsync parses -e honouring quotes.
RSH="ssh -i \"$SSH_KEY\" -o StrictHostKeyChecking=accept-new"
ssh_box() { ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new "$EC2_USER@$EC2_HOST" "$@"; }

echo "==> Sending source to $EC2_HOST:$REMOTE_DIR"
# Only what the image needs. NOT .env: the box has its own, and overwriting it
# with the laptop's would point production at local paths.
rsync -az --delete-after -e "$RSH" \
  --exclude '__pycache__' --exclude '*.pyc' --exclude '.venv*' \
  --exclude '.env' --exclude 'artifacts' \
  backend infra "$EC2_USER@$EC2_HOST:$REMOTE_DIR/"

echo "==> Building on the box (native x86_64)"
ssh_box bash -euo pipefail <<REMOTE
  cd "$REMOTE_DIR"

  # Tag the running image BEFORE the build can overwrite :latest. Doing this by
  # hand is the step that gets skipped exactly when it is needed.
  if docker image inspect $APP:latest >/dev/null 2>&1; then
    docker tag $APP:latest "$APP:previous-\$(date +%Y%m%d%H%M%S)"
    docker tag $APP:latest $APP:previous
    echo "rollback tag: $APP:previous"
  fi

  docker build -f infra/Dockerfile.backend -t $APP:latest .

  # Artifact cache must outlive the container: without this a 'docker rm' costs
  # a 758MB re-download from S3 on the next boot. uid 1001 is the image's user.
  sudo mkdir -p /var/lib/shifamind/fullcode
  sudo chown -R 1001:1001 /var/lib/shifamind

  docker stop $APP 2>/dev/null || true
  docker rm   $APP 2>/dev/null || true
  docker run -d \
    --name $APP \
    --restart unless-stopped \
    -p 8000:8000 \
    -v /var/lib/shifamind/fullcode:/var/lib/shifamind/fullcode \
    --env-file "$REMOTE_DIR/.env" \
    $APP:latest

  docker ps --filter name=$APP
REMOTE

cat <<EOF

==> Container started. The model is NOT loaded yet.

First boot pulls 758MB from S3 into the cache volume, so /api/health/model
answers 503 until it finishes. Watch it:

  ssh -i "\$SSH_KEY" $EC2_USER@$EC2_HOST 'docker logs -f $APP'

Then:

  curl -s http://$EC2_HOST:8000/api/health/model

Expect codes: 7940, concepts: 16227, compose: strict.

Rollback, if needed:
  docker stop $APP && docker rm $APP
  docker run -d --name $APP --restart unless-stopped -p 8000:8000 \\
    --env-file $REMOTE_DIR/.env.50code $APP:50code-rollback
EOF

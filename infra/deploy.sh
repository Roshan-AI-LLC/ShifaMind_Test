#!/usr/bin/env bash
# deploy.sh — Build and deploy ShifaMind backend to AWS EC2 / ECS
# Usage: ./infra/deploy.sh [ecr|ec2]

set -euo pipefail

DEPLOY_TARGET="${1:-ec2}"
AWS_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
APP_NAME="shifamind-api"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "==> ShifaMind backend deploy ($DEPLOY_TARGET)"

# ── Build Docker image ────────────────────────────────────────────────────────
echo "--> Building Docker image..."
# --platform is not optional. The EC2 box is x86_64 (c6a.xlarge); an Apple
# Silicon Mac builds arm64 by default, and the resulting image dies on the
# instance with "exec format error" only AFTER a ~2GB transfer. Buildx emulates
# amd64 through QEMU, which is correct but slow: installing torch this way takes
# a long time. If that is intolerable, build ON the box instead (native, 4 vCPU)
# rather than dropping this flag.
BUILD_PLATFORM="${BUILD_PLATFORM:-linux/amd64}"
docker build --platform "$BUILD_PLATFORM" \
  -f infra/Dockerfile.backend -t "$APP_NAME:$IMAGE_TAG" .

if [[ "$DEPLOY_TARGET" == "ecr" ]]; then
  # ── Push to ECR ───────────────────────────────────────────────────────────
  ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
  ECR_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME"

  echo "--> Authenticating with ECR..."
  aws ecr get-login-password --region "$AWS_REGION" \
    | docker login --username AWS --password-stdin "$ECR_URI"

  echo "--> Tagging and pushing image..."
  docker tag "$APP_NAME:$IMAGE_TAG" "$ECR_URI:$IMAGE_TAG"
  docker push "$ECR_URI:$IMAGE_TAG"

  echo "--> Updating ECS service..."
  aws ecs update-service \
    --cluster shifamind-cluster \
    --service shifamind-api \
    --force-new-deployment \
    --region "$AWS_REGION"

  echo "==> ECS deployment triggered. Monitor at:"
  echo "    https://$AWS_REGION.console.aws.amazon.com/ecs"

elif [[ "$DEPLOY_TARGET" == "ec2" ]]; then
  # ── SSH deploy to EC2 ─────────────────────────────────────────────────────
  EC2_HOST="${EC2_HOST:?Set EC2_HOST env var}"
  EC2_USER="${EC2_USER:-ubuntu}"
  SSH_KEY="${SSH_KEY:-~/.ssh/shifamind.pem}"

  echo "--> Saving image to tarball..."
  docker save "$APP_NAME:$IMAGE_TAG" | gzip > /tmp/shifamind-api.tar.gz

  echo "--> Copying to EC2..."
  scp -i "$SSH_KEY" /tmp/shifamind-api.tar.gz "$EC2_USER@$EC2_HOST:/tmp/"

  echo "--> Loading and restarting on EC2..."
  ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'REMOTE'
    set -e

    # Tag whatever is running now, BEFORE it is replaced. Doing this by hand is
    # a step that gets skipped exactly when it is needed most.
    if docker image inspect shifamind-api:latest >/dev/null 2>&1; then
      docker tag shifamind-api:latest "shifamind-api:previous-$(date +%Y%m%d%H%M%S)"
      docker tag shifamind-api:latest shifamind-api:previous
      echo "tagged rollback image: shifamind-api:previous"
    fi

    docker load < /tmp/shifamind-api.tar.gz

    # The artifact cache must outlive the container: a `docker rm` without this
    # means re-downloading 758MB from S3 on the next boot, which is the whole
    # cold-start cost this server is trying to avoid. uid 1001 is the
    # `shifamind` user the image runs as.
    sudo mkdir -p /var/lib/shifamind/fullcode
    sudo chown -R 1001:1001 /var/lib/shifamind

    docker stop shifamind-api 2>/dev/null || true
    docker rm shifamind-api 2>/dev/null || true
    docker run -d \
      --name shifamind-api \
      --restart unless-stopped \
      -p 8000:8000 \
      -v /var/lib/shifamind/fullcode:/var/lib/shifamind/fullcode \
      --env-file /home/ubuntu/shifamind/.env \
      shifamind-api:latest
    docker ps | grep shifamind
REMOTE

  echo "==> EC2 deployment complete. API at http://$EC2_HOST:8000/api/health"
else
  echo "Unknown target: $DEPLOY_TARGET. Use 'ecr' or 'ec2'."
  exit 1
fi

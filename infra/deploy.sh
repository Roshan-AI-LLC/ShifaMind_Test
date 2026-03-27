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
docker build -f infra/Dockerfile.backend -t "$APP_NAME:$IMAGE_TAG" .

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
    docker load < /tmp/shifamind-api.tar.gz
    docker stop shifamind-api 2>/dev/null || true
    docker rm shifamind-api 2>/dev/null || true
    docker run -d \
      --name shifamind-api \
      --restart unless-stopped \
      -p 8000:8000 \
      --env-file /home/ubuntu/shifamind/.env \
      shifamind-api:latest
    docker ps | grep shifamind
REMOTE

  echo "==> EC2 deployment complete. API at http://$EC2_HOST:8000/api/health"
else
  echo "Unknown target: $DEPLOY_TARGET. Use 'ecr' or 'ec2'."
  exit 1
fi

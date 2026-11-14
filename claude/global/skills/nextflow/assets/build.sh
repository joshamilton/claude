#!/bin/bash
#
# Build and push the custom container images of [project-name].
#
# AWS (ECR):
#   ./docker/build.sh --cloud aws --aws-profile PROFILE --aws-account-id ID --aws-region REGION
# GCP (Artifact Registry):
#   ./docker/build.sh --cloud gcp --gcp-project PROJECT --gcp-region REGION --repo REPOSITORY
#
# Optional: --repo NAME (default: [project-name]), --platform linux/amd64,linux/arm64

set -euo pipefail

# Default values
CLOUD=""
REPO="[project-name]"
PLATFORM=""
AWS_PROFILE=""
AWS_ACCOUNT_ID=""
AWS_REGION=""
GCP_PROJECT=""
GCP_REGION=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --cloud)          CLOUD="$2"; shift 2 ;;
        --repo)           REPO="$2"; shift 2 ;;
        --platform)       PLATFORM="$2"; shift 2 ;;
        --aws-profile)    AWS_PROFILE="$2"; shift 2 ;;
        --aws-account-id) AWS_ACCOUNT_ID="$2"; shift 2 ;;
        --aws-region)     AWS_REGION="$2"; shift 2 ;;
        --gcp-project)    GCP_PROJECT="$2"; shift 2 ;;
        --gcp-region)     GCP_REGION="$2"; shift 2 ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check required arguments
require() {
    if [ -z "$2" ]; then
        echo "Error: $1 is required"
        exit 1
    fi
}

case "$CLOUD" in
    aws)
        require --aws-profile "$AWS_PROFILE"
        require --aws-account-id "$AWS_ACCOUNT_ID"
        require --aws-region "$AWS_REGION"
        REGISTRY_PATH="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        # ECR login
        aws ecr get-login-password --region "$AWS_REGION" --profile "$AWS_PROFILE" | \
            docker login --username AWS --password-stdin "$REGISTRY_PATH"
        ;;
    gcp)
        require --gcp-project "$GCP_PROJECT"
        require --gcp-region "$GCP_REGION"
        REGISTRY_PATH="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}"
        # Artifact Registry login
        gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet
        ;;
    *)
        echo "Error: --cloud must be aws or gcp"
        exit 1
        ;;
esac

# Function to build and push container
build_and_push() {
    local DOCKERFILE=$1
    local IMAGE_NAME=$2
    local IMAGE_TAG=$3
    local FULL_IMAGE_NAME="${REGISTRY_PATH}/${REPO}/${IMAGE_NAME}:${IMAGE_TAG}"

    if [ -n "$PLATFORM" ]; then
        echo "Building and pushing ${IMAGE_NAME} for ${PLATFORM}..."
        docker buildx build \
            --progress=plain \
            --platform "${PLATFORM}" \
            -t "${FULL_IMAGE_NAME}" \
            -f "${DOCKERFILE}" \
            --push .
    else
        echo "Building ${IMAGE_NAME}..."
        docker build \
            --progress=plain \
            -t "${FULL_IMAGE_NAME}" \
            -f "${DOCKERFILE}" .
        echo "Pushing ${IMAGE_NAME}..."
        docker push "${FULL_IMAGE_NAME}"
    fi
}

# Build and push containers
# Add entries for each custom container needed by the pipeline
# Example:
# build_and_push docker/[container_name]/Dockerfile "[container_name]" "[version]"

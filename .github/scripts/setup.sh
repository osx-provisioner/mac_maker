#!/bin/bash

# shellcheck disable=SC2129

set -o pipefail

main() {
  BRANCH_OR_TAG="$(echo "${GITHUB_REF}" | sed 's/refs\/heads\///g' | sed 's/refs\/tags\///g')"
  PROJECT_NAME="mac_maker"
  USERNAME="osx-provisioner"
  echo "PYTHON_VERSION=${PYTHON_VERSION}" >> "$GITHUB_ENV"
  echo "BRANCH_OR_TAG=${BRANCH_OR_TAG}" >> "$GITHUB_ENV"
  echo "WEBHOOK_URL=${WEBHOOK_URL}" >> "$GITHUB_ENV"
  echo "PROJECT_NAME=${PROJECT_NAME}" >> "$GITHUB_ENV"
  echo "NOTIFICATION=${PROJECT_NAME} [${BRANCH_OR_TAG}]" >> "$GITHUB_ENV"
  echo "USERNAME=${USERNAME}" >> "$GITHUB_ENV"
  echo "DOCKER_USERNAME=${DOCKER_USERNAME}" >> "$GITHUB_ENV"
  echo "CD_ENABLED=false" >> "$GITHUB_ENV"
  echo "CD_TEST=false" >> "$GITHUB_ENV"
}

main "$@"

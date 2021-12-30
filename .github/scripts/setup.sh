#!/bin/bash

# shellcheck disable=SC2129

set -eo pipefail

main() {
  BRANCH_OR_TAG="$(echo "${GITHUB_REF}" | sed 's/refs\/heads\///g' | sed 's/refs\/tags\///g')"
  WORKFLOW_URL="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
  echo "PYTHON_VERSION=${PYTHON_VERSION}" >> "$GITHUB_ENV"
  echo "BRANCH_OR_TAG=${BRANCH_OR_TAG}" >> "$GITHUB_ENV"
  echo "WEBHOOK_URL=${WEBHOOK_URL}" >> "$GITHUB_ENV"
  echo "NOTIFICATION=${PROJECT_NAME} [<${WORKFLOW_URL}|${BRANCH_OR_TAG}>]" >> "$GITHUB_ENV"
  echo "DOCKER_USERNAME=${DOCKER_USERNAME}" >> "$GITHUB_ENV"
  echo "SELECTED_PYPI_REPOSITORY=${SELECTED_PYPI_REPOSITORY}" >> "$GITHUB_ENV"
}

main "$@"


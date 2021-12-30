#!/bin/bash

set -eo pipefail

main() {

  if [[ -n "${DOCKER_TOKEN}" ]]; then

    echo "CD_DOCKER_REPO_ENABLED=true" >> "$GITHUB_ENV"

  fi

}

main "$@"

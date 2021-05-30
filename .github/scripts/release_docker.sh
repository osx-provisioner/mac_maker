#!/bin/bash

set -o pipefail

main() {

  if [[ -n "${DOCKER_TOKEN}" ]]; then

    echo "CD_ENABLED=true" >> "$GITHUB_ENV"

  fi

}

main "$@"

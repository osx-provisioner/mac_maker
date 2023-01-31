#!/bin/bash

set -eo pipefail

main() {

  docker-compose build                                        \
    --build-arg BUILD_ARG_PYTHON_VERSION="${PYTHON_VERSION}"  \
    --build-arg BUILD_ARG_CONTAINER_GID="$(id -g)"            \
    --build-arg BUILD_ARG_CONTAINER_UID="$(id -u)"
  docker-compose up -d

}

main "$@"

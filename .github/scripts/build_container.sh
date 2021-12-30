#!/bin/bash

set -eo pipefail

main() {

  docker-compose build --build-arg PYTHON_VERSION="${PYTHON_VERSION}"
  docker-compose up -d

}

main "$@"

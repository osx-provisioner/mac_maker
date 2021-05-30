#!/bin/bash

set -o pipefail

main() {

  docker-compose build --build-arg PYTHON_VERSION="${PYTHON_VERSION}"
  docker-compose up -d

}

main "$@"

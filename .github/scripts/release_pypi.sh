#!/bin/bash

set -o pipefail

main() {

  if [[ -n "${TEST_PYPI_API_TOKEN}" ]]; then

    echo "CD_TEST=true" >> "$GITHUB_ENV"
    docker-compose exec -T "${PROJECT_NAME}" bash -c "                                                 \
      poetry config repositories.testpypi https://test.pypi.org/legacy/                             && \
      poetry publish --build -r testpypi --username __token__ --password \"${TEST_PYPI_API_TOKEN}\"    \
    "
  fi

  if [[ -n "${PYPI_API_TOKEN}" ]]; then

    echo "CD_ENABLED=true" >> "$GITHUB_ENV"
    docker-compose exec -T "${PROJECT_NAME}" bash -c "                                                 \
      poetry publish --build --username __token__ --password \"${PYPI_API_TOKEN}\"                     \
    "

  fi

}

main "$@"

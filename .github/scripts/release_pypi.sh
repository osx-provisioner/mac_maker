#!/bin/bash

set -eo pipefail

main() {

  RELEASE_TYPE="none"

  if [[ -n "${TEST_PYPI_API_TOKEN}" ]] && [[ "${SELECTED_PYPI_REPOSITORY}" == "test" ]]; then
    # If there is an production pypi token, and test_release is active, use test mode
    RELEASE_TYPE="test"
  fi

  if [[ -n "${PYPI_API_TOKEN}" ]] && [[ "${SELECTED_PYPI_REPOSITORY}" == "production" ]]; then
    # If there is an production pypi token, and test_release is off, use production mode
    RELEASE_TYPE="production"
  fi

  case "${RELEASE_TYPE}" in
    "test")
      echo "CD_USE_TEST=true" >> "$GITHUB_ENV"
      docker-compose exec -T "${PROJECT_NAME}" bash -c "                                                 \
        poetry config repositories.testpypi https://test.pypi.org/legacy/                             && \
        poetry publish --build -r testpypi --username __token__ --password \"${TEST_PYPI_API_TOKEN}\"    \
      "
      ;;
    "production")
      echo "CD_USE_PRODUCTION=true" >> "$GITHUB_ENV"
      docker-compose exec -T "${PROJECT_NAME}" bash -c "                                                 \
        poetry publish --build --username __token__ --password \"${PYPI_API_TOKEN}\"                     \
      "
      ;;
    *)
      echo "DEBUG: Cannot perform a test or production release with these credentials and settings."
      echo "DEBUG: SELECTED_PYPI_REPOSITORY was set to: \"${SELECTED_PYPI_REPOSITORY}\""
      ;;
  esac

}

main "$@"

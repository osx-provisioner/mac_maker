#!/bin/bash

set -eo pipefail

main() {

  echo "{}" > package.json
  TAG="$(git tag | sort --version-sort | tail -n 2 | head -n 1)"
  CHANGE_LOG_CONTENT="$(npx -q generate-changelog -f - -t "${TAG}")"

  {
    echo "CHANGE_LOG_CONTENT<<EOF"
    echo "${CHANGE_LOG_CONTENT}"
    echo "EOF"
  } >> "$GITHUB_ENV"

  rm package.json

}

main

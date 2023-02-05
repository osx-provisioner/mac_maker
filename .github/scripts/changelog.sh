#!/bin/bash

set -eo pipefail

main() {

  echo "{}" > package.json
  TAG="$(git tag | sort --version-sort | tail -n 2 | head -n 1)"
  CHANGE_LOG_CONTENT="$(npx -q generate-changelog -f - -t "${TAG}")"

  CHECKLIST_CONTENT=$'\n'
  CHECKLIST_CONTENT+="## Deployment Checklist"$'\n'
  CHECKLIST_CONTENT+="- [] Ensure documentation is accurate"$'\n'
  CHECKLIST_CONTENT+="- [] Ensure readthedocs integration is working"$'\n'

  CHANGE_LOG_CONTENT="${CHANGE_LOG_CONTENT}${CHECKLIST_CONTENT}"

  {
    echo "CHANGE_LOG_CONTENT<<EOF"
    echo "${CHANGE_LOG_CONTENT}"
    echo "EOF"
  } >> "$GITHUB_ENV"

  rm package.json

}

main

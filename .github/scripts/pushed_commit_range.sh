#!/bin/bash

# .github/scripts/pushed_commit_range.sh
# Retrieves the range of the commits in a push, and sets the PUSHED_COMMIT_RANGE environment variables.

# GITHUB_CONTEXT:  The github action context object as an environment variable.

# CI only script

set -eo pipefail


get_all_commits() {
  git rev-list --max-parents=0 HEAD
}


main() {

  PUSHED_COMMIT_RANGE="HEAD~$(echo "$GITHUB_CONTEXT" | jq '.event.commits | length')"

  if [[ "${PUSHED_COMMIT_RANGE}" == "HEAD~0" ]]; then
    PUSHED_COMMIT_RANGE="$(get_all_commits)"
  fi

  set +e
    if ! git rev-parse "${PUSHED_COMMIT_RANGE}"; then
      PUSHED_COMMIT_RANGE="$(get_all_commits)"
    fi
  set -e

  {
    echo "PUSHED_COMMIT_RANGE<<EOF"
    echo "${PUSHED_COMMIT_RANGE}"
    echo "EOF"
  } >> "$GITHUB_ENV"

}

main "$@"

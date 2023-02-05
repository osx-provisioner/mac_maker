#!/bin/bash

# .github/scripts/upload_asset.sh
# Upload an asset to a Github release.

# FILE_PATH: The filename to upload.
# GITHUB_TOKEN: The Github authentication token to use.
# UPLOAD_URL: The release's upload url.

# CI only script.

set -eo pipefail

main() {

  UPLOAD_URL="${UPLOAD_URL/\{?name,label\}/}"

  curl --fail -X POST                                                  \
       -H "Content-Length: $(stat --format="%s" "${FILE_PATH}")"       \
       -H "Content-Type: $(file -b --mime-type "${FILE_PATH}")"        \
       -H "X-GitHub-Api-Version: 2022-11-28"                           \
       -T "${FILE_PATH}"                                               \
       -H "Authorization: token ${GITHUB_TOKEN}"                       \
       -H "Accept: application/vnd.github.v3+json"                     \
       "${UPLOAD_URL}?name=$(basename "${FILE_PATH}")"                 | cat

}

main "$@"

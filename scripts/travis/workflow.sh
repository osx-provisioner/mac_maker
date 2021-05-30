#!/bin/bash

set -e

main() {

  ./scripts/build.sh pyenv "${PYTHON}" > /dev/null

  eval $(pyenv init --path);
  pip install poetry wheel

  ./scripts/build.sh binary "${VERSION}"
  ./dist/mac_maker version

  if [[ "${TRAVIS_BRANCH}" == v* ]]; then
    ./scripts/travis/upload.sh github_api_token="${GITHUB_TOKEN}" owner="osx-provisioner" repo="mac_maker" tag="${TRAVIS_BRANCH}" filename="./dist/mac_maker_${VERSION}_$(uname -m).tar.gz"
  fi

}

main "$@"

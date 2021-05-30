#!/bin/bash

set -e

wrong_platform(){
  echo "This script needs to be run on an OSX machine."
  exit 127
}

wrong_args(){
  echo "Usages: "
  echo "./scripts/build pyenv [version (3.8.10)]"
  echo "./scripts/build binary [version (10.14)]"
  exit 127
}

binary() {

  poetry build
  poetry run pip install ./dist/mac_maker-*-py3-none-any.whl
  poetry run pyinstaller --onefile build.spec

  pushd dist || exit 127
    VERSION_NAME="${2}_$(uname -m)"
    mkdir "mac_maker_${VERSION_NAME}"
    cp mac_maker "mac_maker_${VERSION_NAME}"
    tar cvzf "mac_maker_${VERSION_NAME}.tar.gz" "mac_maker_${VERSION_NAME}"
    rm -rf "mac_maker_${VERSION_NAME}"
  popd || true
}

python() {

  if [[ -z "${TRAVIS_BRANCH}" ]]; then
    brew install pyenv coreutils openssl readline sqlite3 xz zlib
  else
    brew update
    brew upgrade pyenv coreutils openssl readline sqlite3 xz zlib
  fi

  env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install "${2}"
  pyenv local "${2}"

}

main() {

  if [[ "$OSTYPE" != "darwin"* ]]; then
    wrong_platform
  fi

  case ${1} in

    pyenv)
      python "$@"
      ;;
    binary)
      binary "$@"
      ;;
    *)
      wrong_args
      ;;
  esac

}

main "$@"

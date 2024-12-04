#!/bin/bash

set -e

PYENV_VERSION_TAG="v2.4.20"

wrong_platform(){
  echo "This script needs to be run on an OSX machine."
  exit 127
}

wrong_args(){
  echo "Usages: "
  echo "./scripts/build pyenv [Python Version (3.8.16)]"
  echo "./scripts/build binary [OS Version (10.14)] [Mac Maker Version (0.0.5)]"
  exit 127
}

build_binary() {

  poetry install --only=main
  poetry run pyinstaller build.spec

  pushd dist || exit 127
    VERSION_NAME="${2}_$(uname -m)"
    VERSION_TAG=${3-unknown}
    BASE_NAME="mac_maker_${VERSION_NAME}_${VERSION_TAG}"
    mkdir "${BASE_NAME}"
    cp mac_maker "${BASE_NAME}"
    tar cvzf "${BASE_NAME}.tar.gz" "${BASE_NAME}"
    rm -rf "${BASE_NAME}"
  popd || true

}

build_python() {

  env HOMEBREW_NO_AUTO_UPDATE=1 brew install coreutils openssl readline sqlite3 xz zlib
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  pushd ~/.pyenv
    git checkout "${PYENV_VERSION_TAG}"
    src/configure
    make -C src
  popd

  env PYTHON_CONFIGURE_OPTS="--enable-framework" ~/.pyenv/bin/pyenv install "${2}"
  ~/.pyenv/bin/pyenv local "${2}"

}

main() {

  if [[ "$OSTYPE" != "darwin"* ]]; then
    wrong_platform
  fi

  case ${1} in

    pyenv)
      build_python "$@"
      ;;
    binary)
      build_binary "$@"
      ;;
    *)
      wrong_args
      ;;
  esac

}

main "$@"

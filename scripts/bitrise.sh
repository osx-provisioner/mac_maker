#!/bin/bash

export HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1

set -eo pipefail

# Initialize Environment
rm -rf ~/.pyenv
mkdir "${BITRISE_DEPLOY_DIR}"

# Build Python Distribution
bash scripts/build.sh pyenv "${PYTHON_VERSION}"

# Build Mac Maker Binary
eval "$(~/.pyenv/bin/pyenv init --path)"
pip install poetry
BUILD_NAME="${BITRISE_GIT_TAG}"
if [[ -z "${BUILD_NAME}" ]]; then
  BUILD_NAME="${BITRISE_GIT_BRANCH}"
fi
bash scripts/build.sh binary "${OS_VERSION}" "${BUILD_NAME}"

# Move Built Binary to Artifacts Folder
mv ./dist/*.tar.gz "${BITRISE_DEPLOY_DIR}"

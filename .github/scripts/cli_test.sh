#!/bin/bash

set -o pipefail

main() {

  dev build-docs
  dev build-wheel
  diff <(echo "Current Configuration: ${PIB_CONFIG_FILE_LOCATION}") <(dev config-location)
  diff <(dev config-show) "${PIB_CONFIG_FILE_LOCATION}"
  dev coverage
  dev fmt
  dev leaks
  dev lint
  dev reinstall-requirements
  dev sectest
  dev setup-bash
  dev setup
  dev test
  dev version

}

main "$@"

#!/bin/bash

set -o pipefail

main() {

  shellcheck ./.github/scripts/*.sh
  shellcheck ./mac_maker/*.sh
  shellcheck ./scripts/*.sh
  shellcheck ./scripts/hooks/*

}

main "$@"

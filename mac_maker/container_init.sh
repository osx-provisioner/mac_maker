#!/bin/bash

DEVELOPMENT() {
  pushd "mac_maker" || exit 127
  while true; do sleep 1; done
}

PRODUCTION() {
  mac_maker
}

eval "${ENVIRONMENT}"

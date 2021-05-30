#!/bin/bash

DEVELOPMENT() {
  pushd "mac_maker" || exit 127
  while true; do sleep 1; done
}

PRODUCTION() {
  pushd "mac_maker" || exit 127
  while true; do sleep 1; done
}

eval "${ENVIRONMENT}"

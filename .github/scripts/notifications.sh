#!/bin/bash

# Takes two text arguments
# Message Format: <ARG1>: <ARG2>

[[ -z ${WEBHOOK_URL} ]] && exit 0
curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"${1}: ${2}\"}" "${WEBHOOK_URL}"

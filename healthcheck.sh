#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"
curl --fail --silent "${BASE_URL}/health"; echo
curl --fail --silent "${BASE_URL}/ready"; echo

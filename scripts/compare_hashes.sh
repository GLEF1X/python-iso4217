#!/bin/bash

# Terminate the script on command fails
set -o nounset

DATA_SOURCE="${DATA_SOURCE_URL:-https://datahub.io/core/currency-codes/r/codes-all.json}"
QUERY_TIMEOUT_SECONDS="${QUERY_TIMEOUT_SECONDS:-20}"

echo "Use $DATA_SOURCE to retrieve currency data"
curl -H "Content-Type: application/json" --max-time $QUERY_TIMEOUT_SECONDS -o currencies.json $DATA_SOURCE

if cmp --silent -- ./iso4217/data/currencies.json currencies.json; then
  echo "Files contents are identical, nothing to update, exiting..."
  exit 1
else
  echo "currencies db has been changed, updating currencies.json" >&2
  cat currencies.json >./iso4217/data/currencies.json
fi

rm -f currencies.json

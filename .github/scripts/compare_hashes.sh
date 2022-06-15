#!/bin/bash

base_data_path=iso4217/data

curl https://datahub.io/core/currency-codes/r/codes-all.json -o updated_db.json

currency_db_hash=$(openssl dgst -sha256 <updated_db.json)
old_hash=$(cat $base_data_path/hash)

# fail if hashes are equal, because we don't need to update package
[ "$currency_db_hash" == "$old_hash" ] && rm -f updated_db.json && exit 1

cat update_db.json >$base_data_path/currencies.json
echo $currency_db_hash >$base_data_path/hash

rm -f update_db.json

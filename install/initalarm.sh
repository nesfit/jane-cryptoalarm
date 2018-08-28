#!/bin/bash
echo "Initializing cryptoalarm block index within network $1"
docker run --network="$1" -t cryptoalarm-app /bin/sh -c "./run.py --init"

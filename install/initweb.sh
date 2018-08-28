#!/bin/bash
echo "Initializing cryptoalarm web database within network $1"
docker run --network="$1" -v `pwd`/volumes/web:/var/www -t cryptoalarm-web /bin/sh -c "php artisan migrate && php artisan db:seed"

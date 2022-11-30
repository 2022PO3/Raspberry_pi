#!/bin/bash

libcamera-still --immediate -o $1 -n --verbose=0 --hflip --vflip
curl -F "file=@$1" -H 'charset:UTF8;' -H 'PO3-ORIGIN: rpi' -H "PO3-RPI-KEY: $RPI_KEY" -H "PO3-GARAGE-ID: 1" "https://po3backend.ddns.net/api/images" 
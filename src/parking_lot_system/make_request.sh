#!/bin/bash

curl -H 'charset:UTF8;' -H 'PO3-ORIGIN: rpi' -H "PO3-RPI-KEY: $RPI_KEY" -d '{"garageId":1,"parkingLotNo":"$1", "occupied": $2}' "https://po3backend.ddns.net/api/rpi-parking-lot"  
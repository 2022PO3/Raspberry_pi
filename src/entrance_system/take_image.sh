#!/bin/bash
# Send a dummy request to prevent that the real request is a cold request.
curl --silent -H 'charset:UTF8;' -H 'PO3-ORIGIN: rpi' -H "PO3-RPI-KEY: $RPI_KEY" -H "PO3-GARAGE-ID: 11" -d "{\"garageId\": 11, \"licencePlate\": \"0AAA000\"}" "https://po3backend.ddns.net/api/images" > resp.txt &

# Take the image.
libcamera-still --immediate -o $1 -n --verbose=0 --hflip --vflip

# Send the image to the Google Vision API and parse the response with a licence plate regex.
LP=`gcloud ml vision detect-text $IMAGE_PATH | jq '.responses[].textAnnotations[0].description' | sed -e 's/[[:punct:]]//g' | grep -oE '[[:digit:]][A-Z]{3}[[:digit:]]{3}'`
# Send the licence plate string to the Backend.
curl --silent -H 'charset:UTF8;' -H 'PO3-ORIGIN: rpi' -H "PO3-RPI-KEY: $RPI_KEY" -H "PO3-GARAGE-ID: 11" -d "{\"garageId\": 11, \"licencePlate\": \"$LP\"}" "https://po3backend.ddns.net/api/images"

# Remove the temporary files.
rm resp.txt
rm $1
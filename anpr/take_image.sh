libcamera-still --immediate -o $1 -n --verbose=0 --hflip --vflip
curl -F "file=@$1" -H 'charset:UTF8;' -H 'PO3-ORIGIN: rpi' -H "PO3-RPI-KEY: $RPI_KEY" -H "PO3-GARAGE-ID: 1" "http://192.168.49.1:8000/api/images" 


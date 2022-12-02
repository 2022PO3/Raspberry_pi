#!/bin/bash

echo "Start entrance system..."
python src/entrance_system/main_pi2.py &

echo "Start parking lot system..."
python src/parking_lot_system/main_pi2.py &

echo "Startup completed. Opening log..."
tail -f ~/Raspberry_Pi/rpi_garage.log

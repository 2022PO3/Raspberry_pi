#!/bin/bash

echo "Start entrance system..."
python src/entrance_system/main_pi2.py &
sleep 1

echo "Start parking lot system..."
python src/parking_lot_system/main_pi2.py &
sleep 1

echo "Startup completed. Opening log..."
sleep 1
tail -f rpi_garage.log

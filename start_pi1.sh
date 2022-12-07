#!/bin/bash

echo "Start entrance system..."
python src/entrance_system/main_pi1.py &
sleep 1
echo "Entrance system running with PID `pgrep -f src/entrance_system/main_pi1.py`"


echo "Start parking lot system..."
python src/parking_lot_system/main_pi1.py &
sleep 1
echo "Parking lot system running with PID `pgrep -f src/parking_lot_system/main_pi1.py`"

echo "Startup completed. Opening log..."
sleep 1
tail -f rpi_garage.log

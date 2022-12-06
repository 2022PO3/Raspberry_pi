#!/bin/bash

echo "Start entrance system..."
python ~/Raspberry_Pi/src/entrance_system/main_pi1.py &

echo "Start parking lot system..."
python ~/Raspberry_Pi/src/parking_lot_sytem/main_pi1.py &

echo "Start 7 segment display system..."
python ~/Raspberry_Pi/src/parking_lot_system/7_segment_display_control.py

echo "Startup completed. Opening log..."
tail -f ~/Raspberry_Pi/rpi_garage.log

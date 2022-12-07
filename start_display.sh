#!/bin/bash

function ctrl_c() {
    echo "Exiting program. Shutting down services..."
    sudo kill $1
    echo "Shut down PID ${1}."
}

stty -echoctl
trap 'ctrl_c ${pid_display}' SIGINT

echo "Starting display..."
python src/parking_lot_system/7_segment_display_control.py &
sleep 1
pid_display=$(pgrep -f src/parking_lot_system/7_segment_display_control.py)
echo "Display runing as PID ${pid_display}."

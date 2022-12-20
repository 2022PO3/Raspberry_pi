#!/bin/bash

function ctrl_c() {
    echo "Exiting program. Shutting down services..."
    sudo kill $1
    sudo kill $2
    sudo kill $3
    echo "Shut down PID ${1}, ${2} and ${3}."
}

stty -echoctl
trap 'ctrl_c ${pid_entrance} ${pid_parking} ${pid_display}' SIGINT
rm -f rpi_garage.log


echo "Start entrance system..."
python src/entrance_system/main_pi${1}.py &
sleep 1
pid_entrance=$(pgrep -f src/entrance_system/main_pi${1}.py)
echo "Entrance system running with PID ${pid_entrance}"

echo "Start parking lot system..."
python src/parking_lot_system/main_pi${1}.py &
sleep 1
pid_parking=$(pgrep -f src/parking_lot_system/main_pi${1}.py)
echo "Parking lot system running with PID ${pid_parking}"

if [ ${1} -eq 1 ]; then
    echo "Start display..."
    python src/parking_lot_system/display_control.py &
    sleep 1
    pid_display=$(pgrep -f src/parking_lot_system/display_control.py)
    echo "Display running with PID ${pid_display}."
    sleep 1
fi

echo "Startup completed. Opening log..."
sleep 3
tail -f --lines=50 rpi_garage.log

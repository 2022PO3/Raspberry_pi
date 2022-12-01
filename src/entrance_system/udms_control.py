import time
import os
import requests
import subprocess
import RPi.GPIO as GPIO
import main1
from servo_control import open_barrier, close_barrier

logger = main1.get_logger("udms_control")


def setup_udms(trig_pin: int, echo_pin: int, sensor_no: int) -> None:
    """
    Sets up the udms on the `trig_pin` and `echo_pin`.
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    time.sleep(2)
    logger.info(f"Setup of ultrasonic sensor {sensor_no} completed.")


def calculate_distance(trig_pin: int, echo_pin: int, time_delta: int) -> float:
    """
    Reads on the distance measuring of the udms connected on the `trig_pin` and `echo_pin`.
    """
    time.sleep(time_delta)

    GPIO.output(trig_pin, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(trig_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    return round(pulse_duration * 17150, 2)


###################
# Entrance system #
###################
def take_picture(
    distance: float,
    sensor_state: bool,
    sensor_no: int,
    servo,
    servo_no: int,
) -> bool:
    """
    Takes picture when the distance is small enough (car is on top of the sensor). The
    `sensor_state` variable contains the boolean if a car is on top of the sensor. If it is,
    the sensor will no longer log the fact that the car is on top of the sensor, except when
    the car leaves the sensor. This way, only two log messages are written: one when the car
    enters the sensor and one when it leaves. The return value is the newly assigned state.
    """
    if distance < 5 and not sensor_state:
        logger.info(f"Car entered sensor {sensor_no}")
        subprocess.run(["bash", "take_image.sh", "image.jpg"])
        logger.info(f"Took image of car on sensor {sensor_no}")
        open_barrier(servo, servo_no)
        return not sensor_state
    elif distance >= 5 and sensor_state:
        logger.info(f"Car left sensor {sensor_no}")
        time.sleep(2)
        close_barrier(servo, servo_no)
        return not sensor_state
    else:
        return sensor_state


######################
# Parking lot system #
######################
def update_state(sensor_state: list[bool], distance: float) -> None:
    """
    Updates the given state of a UDMS and returns the newly updated state. This has the effect
    that first element is pushed to the list, deleting the last element.
    """
    sensor_state = [True if distance < 5 else False] + sensor_state[:2]


def make_request(
    sensor_state: list[bool], parking_no: int, garage_id: int
) -> list[bool]:
    """
    Makes request about the state of the parking lot to the Backend.
    """
    url = "https://po3backend.ddns.net/api/rpi-parking-lot"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI-KEY"]}
    body = {"garageId": garage_id, "parkingLotNo": parking_no}
    if sensor_state == [True] * 3:
        body |= {"occupied": True}
        requests.post(url, body, headers=headers)
        logger.info(f"Sent request that parking lot {parking_no} is occupied.")
    elif sensor_state == [False] * 3:
        body |= {"occupied": False}
        requests.post(url, body, headers=headers)
        logger.info(f"Sent request that parking lot {parking_no} is emptied.")
    return sensor_state

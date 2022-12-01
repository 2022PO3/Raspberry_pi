import time
import os
import requests
import led_control
import RPi.GPIO as GPIO
import main

logger = main.get_logger("udms_control")


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


######################
# Parking lot system #
######################
def update_state(sensor_state: list[bool], distance: float) -> list[bool]:
    """
    Updates the given state of a UDMS and returns the newly updated state. This has the effect
    that first element is pushed to the list, deleting the last element.
    """
    sensor_state = [True if distance < 5 else False] + sensor_state[:2]
    return sensor_state


def make_request(
    sensor_state: list[bool], led_pin_no, parking_no: int, garage_id: int
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
        led_control.turn_on_red(led_pin_no, parking_no)
    elif sensor_state == [False] * 3:
        body |= {"occupied": False}
        requests.post(url, body, headers=headers)
        logger.info(f"Sent request that parking lot {parking_no} is emptied.")
        led_control.turn_on_green(led_pin_no, parking_no)
    return sensor_state

import time
import os
from requests import post, Response

import RPi.GPIO as GPIO

from logger import get_logger, log
from servo_control import open_barrier, close_barrier, Servo
from camera_control import detect_licence_plate

logger = get_logger("udms_control")

GARAGE_ID = 11


def setup_udms(trig_pin: int, echo_pin: int, *, system: str) -> None:
    """
    Sets up the udms on the `trig_pin` and `echo_pin`.
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    time.sleep(1)
    log(f"Setup of {system} sensor completed.", logger)


def calculate_distance(trig_pin: int, echo_pin: int) -> float:
    """
    Reads on the distance measuring of the udms connected on the `trig_pin` and `echo_pin`.
    """
    GPIO.output(trig_pin, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(trig_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    return round(pulse_duration * 17150, 2)


def send_licence_plate(licence_plate: str, garage_id: int) -> Response:
    url = f"{os.getenv('SERVER_URL')}api/rpi/licence-plates"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = post(
        url,
        data={"licencePlate": licence_plate, "garageId": garage_id},
        headers=headers,
    )

    return response


def can_enter(response: Response) -> bool:
    return response.status_code == 200


def run_enter_detection(
    distance: float,
    sensor_state: bool,
    servo: Servo,
    servo_state: bool,
    *,
    system: str,
) -> tuple[bool, bool]:
    """
    Takes picture when the distance is small enough (car is on top of the sensor). The
    `sensor_state` variable contains the boolean if a car is on top of the sensor. If it is,
    the sensor will no longer log the fact that the car is on top of the sensor, except when
    the car leaves the sensor. This way, only two log messages are written: one when the car
    enters the sensor and one when it leaves. The return value isa tuple of the sensor state
    and the servo state.
    """
    if distance < 10 and not sensor_state:
        log(f"Car entered {system} sensor.", logger)
        licence_plate_system = detect_licence_plate()
        log("Posting request to backend.", logger)
        resp = send_licence_plate(licence_plate_system, GARAGE_ID)
        print(resp.text)
        if can_enter(resp):
            servo_state = open_barrier(servo, servo_state, system=system)
        log("Car cannot enter the parking", logger)
        return not sensor_state, servo_state
    elif distance >= 5 and sensor_state:
        log(f"Car left {system} sensor.", logger)
        time.sleep(2)
        servo_state = close_barrier(servo, servo_state, system=system)
        return not sensor_state, servo_state
    else:
        return sensor_state, servo_state

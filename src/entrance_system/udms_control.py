import time
import subprocess
import os
import RPi.GPIO as GPIO

from logger import get_logger, justify_logs
from servo_control import open_barrier, close_barrier, Servo

logger = get_logger("udms_control")


def setup_udms(trig_pin: int, echo_pin: int, *, system: str) -> None:
    """
    Sets up the udms on the `trig_pin` and `echo_pin`.
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    time.sleep(1)
    logger.info(justify_logs(f"Setup of {system} sensor completed.", 44))


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
    logger.info(f"Distance: {str(round(pulse_duration * 17150, 2))}")
    return round(pulse_duration * 17150, 2)


def take_picture(
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
    if distance < 5 and not sensor_state:
        logger.info(justify_logs(f"Car entered {system} sensor.", 44))
        try:
            output = subprocess.check_output(
                [
                    "bash",
                    f"{os.environ['HOME']}/raspberry_pi/src/entrance_system/take_image.sh",
                    "image.jpg",
                ]
            )
            logger.info(justify_logs(f"Took image of {system} car.", 44))
            if "success" in str(output).lower():
                servo_state = open_barrier(servo, servo_state, system=system)
        except subprocess.CalledProcessError:
            logger.info(justify_logs(f"Image taking on {system} failed.", 44))

        else:
            logger.info(justify_logs(f"Licence plate check of {system} failed.", 44))
        return not sensor_state, servo_state
    elif distance >= 5 and sensor_state:
        logger.info(justify_logs(f"Car left {system} sensor.", 44))
        time.sleep(2)
        servo_state = close_barrier(servo, servo_state, system=system)
        return not sensor_state, servo_state
    else:
        return sensor_state, servo_state

import logging
import subprocess
import RPi.GPIO as GPIO
import time

# Config of the logger for logging entrances and exits of the garage.
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename="anpr_garage.log",
    filemode="w",
)
logger = logging.getLogger("anpr_garage")


def setup_udms(trig_pin: int, echo_pin: int, sensor_no: int) -> None:
    """
    Sets up the udms on the `trig_pin` and `echo_pin`.
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    time.sleep(2)
    logger.info(f"Setup for sensor {sensor_no} completed.")


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


def take_picture(distance: float, sensor_state: bool, sensor_no: int) -> bool:
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
        return not sensor_state
    elif distance >= 5 and sensor_state:
        logger.info(f"Car left sensor {sensor_no}")
        return not sensor_state
    else:
        return sensor_state


if __name__ == "__main__":
    ECHO_PIN1 = 11
    TRIG_PIN1 = 7
    ECHO_PIN2 = 5
    TRIG_PIN2 = 3

    sensor1_state = False
    sensor2_state = False

    setup_udms(TRIG_PIN1, ECHO_PIN1, 1)
    setup_udms(TRIG_PIN2, ECHO_PIN2, 2)
    logger.info("Setup completed starting to measure distances.")
    while True:
        sensor1_state = take_picture(
            calculate_distance(TRIG_PIN1, ECHO_PIN1, 1), sensor1_state, 1
        )
        sensor2_state = take_picture(
            calculate_distance(TRIG_PIN2, ECHO_PIN2, 1), sensor2_state, 2
        )

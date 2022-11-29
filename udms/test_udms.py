import sys
import time
import logging
import subprocess
import RPi.GPIO as GPIO
from led_controll import *
from display_controll import *



# Config of the logger for logging entrances and exits of the garage.
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename="anpr_garage.log",
    filemode="w",
)
logger = logging.getLogger("anpr_garage")
logger.addHandler(logging.StreamHandler(sys.stdout))

# define entrance/exit sensor pins
ECHO_PIN1 = 11
TRIG_PIN1 = 7
ECHO_PIN2 = 5
TRIG_PIN2 = 3

# define parking sensor pins
ECHO_PIN_P1 =
TRIG_PIN_P1 =
ECHO_PIN_P2 =
TRIG_PIN_P2 =
ECHO_PIN_P3 =
TRIG_PIN_P3 =
ECHO_PIN_P4 =
TRIG_PIN_P4 =
ECHO_PIN_P5 =
TRIG_PIN_P5 =
ECHO_PIN_P6 =
TRIG_PIN_P6 =


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


def is_car_in_parking(distance: float, sensor_state: bool, parking_no: int) -> bool:
    """
    Gives back True if thers is a car detected in a parking space and false if not.
    """
    if distance < 5 and not sensor_state:
        logger.info(f"Car entered parking {parking_no}")
        return not sensor_state
    elif distance >= 5 and sensor_state:
        logger.info(f"Car left parking {parking_no}")
        return not sensor_state
    else:
        return sensor_state


if __name__ == "__main__":

    sensor1_state = False
    sensor2_state = False

    parking1_state = False
    parking2_state = False
    parking3_state = False
    parking4_state = False
    parking5_state = False
    parking6_state = False

    setup_udms(TRIG_PIN1, ECHO_PIN1, 1)
    setup_udms(TRIG_PIN2, ECHO_PIN2, 2)

    setup_udms(TRIG_PIN_P1, ECHO_PIN_P2, 2)
    setup_udms(TRIG_PIN_P2, ECHO_PIN_P2, 2)
    setup_udms(TRIG_PIN_P3, ECHO_PIN_P3, 2)
    setup_udms(TRIG_PIN_P4, ECHO_PIN_P4, 2)
    setup_udms(TRIG_PIN_P5, ECHO_PIN_P5, 2)
    setup_udms(TRIG_PIN_P6, ECHO_PIN_P6, 2)

    setup_leds()

    setup_display()
    reset_display()

    logger.info("Setup completed starting to measure distances.")
    while True:
        # sensors entrance/exit
        sensor1_state = take_picture(
            calculate_distance(TRIG_PIN1, ECHO_PIN1, 1), sensor1_state, 1
        )
        sensor2_state = take_picture(
            calculate_distance(TRIG_PIN2, ECHO_PIN2, 1), sensor2_state, 2
        )

        # servo motors


        # sensors parking
        parking1_state = is_car_in_parking(
            calculate_distance(TRIG_PIN_P1, ECHO_PIN_P1, 1), parking1_state, 1
        )
        parking2_state = is_car_in_parking(
            calculate_distance(TRIG_PIN_P2, ECHO_PIN_P2, 2), parking2_state, 2
        )
        parking3_state = is_car_in_parking(
            calculate_distance(TRIG_PIN_P3, ECHO_PIN_P3, 3), parking3_state, 3
        )
        parking4_state = is_car_in_parking(
            calculate_distance(TRIG_PIN_P4, ECHO_PIN_P4, 4), parking4_state, 4
        )
        parking5_state = is_car_in_parking(
            calculate_distance(TRIG_PIN_P5, ECHO_PIN_P5, 5), parking5_state, 5
        )
        parking6_state = is_car_in_parking(
            calculate_distance(TRIG_PIN_P6, ECHO_PIN_P6, 6), parking6_state, 6
        )

        # available spots
        "reserving a parking spot still needs to be added"
        available_spots = [parking1_state, parking2_state, parking3_state, parking4_state, parking5_state, parking6_state]

        # change leds
        change_leds(available_spots)

        # change display
        change_display(available_spots)

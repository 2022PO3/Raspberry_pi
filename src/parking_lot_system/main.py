import RPi.GPIO as GPIO
import time
from logger import get_logger


logger = get_logger("parking_lot_system")

#####################
# Defining the pins #
#####################
# LED pins in the format `parking_lot_no: pin_no`. The pins are in the order [RED, GREEN].
PARKING_LED_PINS = {
    1: (23, 29),
    2: (31, 33),
    3: (35, 37),
}

# Pins for the ultrasonic sensors (the number refers to the parking lot number). The pins are
# in the order [TRIG, ECHO].
UDMS_PINS = {
    1: (11, 3),
    2: (13, 5),
    3: (15, 7),
}

PULSE_FREQUENCY = 50

GARAGE_ID = 11


def _setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


def run_parking_lot_system(
    udms_pins: dict[int, tuple[int, int]],
    parking_led_pins: dict[int, tuple[int, int]],
    *,
    pi_no: int,
) -> None:
    import udms_control
    import led_control

    rng = range(1, 4) if pi_no else range(4, 7)

    # The states are an array of length 2. This prevents false positives. Only when the sensor
    # detects a car (or no car) for two consecutive times, the car will be detected. The first
    # element indicates most recent measurement.
    state_dict = {i: [False] * 2 for i in rng}

    _setup_board()
    for i in rng:
        udms_control.setup_udms(udms_pins[i], i)
        led_control.setup_led(parking_led_pins[i], i)
    logger.info("Setup of parking lot system completed successfully.")
    try:
        while True:
            for i in rng:
                distance = udms_control.calculate_distance(udms_pins[i], 1)
                state_dict[i] = udms_control.update_parking_lot(
                    state_dict[i],
                    distance,
                    parking_led_pins[i],
                    i,
                    GARAGE_ID,
                )
                time.sleep(0.14)
    except KeyboardInterrupt:
        GPIO.cleanup()

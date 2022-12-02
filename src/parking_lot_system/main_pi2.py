import RPi.GPIO as GPIO
import logging
import time

#################
# Logger config #
#################
def get_logger(name: str) -> logging.Logger:
    log_format = "%(asctime)s: %(message)s (%(name)8s)"
    logging.basicConfig(
        level=logging.INFO, format=log_format, filename="rpi_garage.log", filemode="w"
    )
    return logging.getLogger(name)


logger = get_logger("parking_lot_system")

#####################
# Defining the pins #
#####################
# LED pins in the format `parking_lot_no: pin_no`. The pins are in the order [RED, GREEN].
PARKING_LED_PINS = {
    4: (23, 29),
    5: (31, 33),
    6: (35, 37),
}

# Pins for the ultrasonic sensors (the number refers to the parking lot number). The pins are in
# the order [TRIG, ECHO].
UDMS_PINS = {
    4: (11, 3),
    5: (13, 5),
    6: (15, 7),
}

PULSE_FREQUENCY = 50

GARAGE_ID = 11

##################
# Setting states #
##################
# The states are an array of length 2. This prevents false positives. Only when the sensor
# detects a car (or no car) for two consecutive times, the car will be detected. The first
# element indicates most recent measurement.
state_dict = {i: [False] * 2 for i in range(4, 7)}


def setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    import udms_control
    import led_control

    setup_board()
    for i in range(4, 7):
        udms_control.setup_udms(UDMS_PINS[i], i)
        led_control.setup_led(PARKING_LED_PINS[i], i)
    logger.info("Setup of parking lot system completed successfully.")
    try:
        while True:
            for i in range(4, 7):
                distance = udms_control.calculate_distance(UDMS_PINS[i], 1)
                state_dict[i] = udms_control.update_parking_lot(
                    state_dict[i],
                    distance,
                    PARKING_LED_PINS[i],
                    i,
                    GARAGE_ID,
                )
                time.sleep(0.14)
    except KeyboardInterrupt:
        GPIO.cleanup()
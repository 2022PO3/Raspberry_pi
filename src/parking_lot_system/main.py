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
# LED pins in the format `parking_lot_no: pin_no`.
PARKING_LED_PINS = {1: 37, 2: 40, 3: 3, 4: 22, 5: 38}

# Pins for the ultrasonic sensors (the number refers to the parking lot number).
UDMS_PINS = {
    1: [11, 13],
    2: [23, 29],
    3: [7, 12],
    4: [32, 36],
    5: [15, 16],
    6: [35, 18],
}

PULSE_FREQUENCY = 50

GARAGE_ID = 1

##################
# Setting states #
##################
# The states are an array of length 2. This prevents false positives. Only when the sensor
# detects a car (or no car) for two consecutive times, the car will be detected. The first
# element indicates most recent measurement.
state_dict = {i: [False] * 2 for i in range(1, 7)}


def setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    import udms_control
    import led_control

    setup_board()
    for i in range(1, 2):
        udms_control.setup_udms(UDMS_PINS[i], i)
        led_control.setup_led(PARKING_LED_PINS[i])
    logger.info("Setup of parking lot system completed successfully.")

    while True:
        for i in range(1, 2):
            distance = udms_control.calculate_distance(UDMS_PINS[i], 1)
            print(distance)
            print(state_dict[1])
            state_dict[i] = udms_control.update_parking_lot(
                state_dict[i],
                distance,
                PARKING_LED_PINS[i],
                i,
                GARAGE_ID,
            )
            time.sleep(0.14)

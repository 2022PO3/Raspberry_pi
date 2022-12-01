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
# LED pins
PARKING1_LED_PIN = 37
PARKING2_LED_PIN = 40
PARKING3_LED_PIN = 3
PARKING4_LED_PIN = 22
PARKING5_LED_PIN = 5
PARKING6_LED_PIN = 38

# Pins for the ultrasonic sensors (the number refers to the parking lot number).
TRIG_PIN1 = 11
ECHO_PIN1 = 13
TRIG_PIN2 = 23
ECHO_PIN2 = 29
TRIG_PIN3 = 7
ECHO_PIN3 = 12
TRIG_PIN4 = 32
ECHO_PIN4 = 36
TRIG_PIN5 = 15
ECHO_PIN5 = 16
TRIG_PIN6 = 35
ECHO_PIN6 = 18

PULSE_FREQUENCY = 50

GARAGE_ID = 1

##################
# Setting states #
##################
# The states are an array of length 2. This prevents false positives. Only when the sensor
# detects a car (or no car) for two consecutive times, the car will be detected. The first
# element indicates most recent measurement.
sensor1_state = [False] * 2
sensor2_state = [False] * 2
sensor3_state = [False] * 2
sensor4_state = [False] * 2
sensor5_state = [False] * 2
sensor6_state = [False] * 2


def setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    import udms_control
    import led_control

    setup_board()
    for i in range(1, 7):
        udms_control.setup_udms(eval(f"TRIG_PIN{i}"), eval(f"ECHO_PIN{i}"), i)
        led_control.setup_led(eval(f"PARKING{i}_LED_PIN"))
    logger.info("Setup of parking lot system completed successfully.")

    while True:
        for i in range(1, 7):
            distance = udms_control.calculate_distance(
                eval(f"TRIG_PIN{i}"), eval(f"ECHO_PIN{i}"), 1
            )
            udms_control.update_parking_lot(
                eval(f"sensor{i}_state"),
                distance,
                eval(f"PARKING{i}_LED_PIN"),
                i,
                GARAGE_ID,
            )
            time.sleep(0.14)

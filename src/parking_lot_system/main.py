import RPi.GPIO as GPIO
import logging


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
PARKING2_LED_PIN = 2
PARKING3_LED_PIN = 3
PARKING4_LED_PIN = 4
PARKING5_LED_PIN = 5
PARKING6_LED_PIN = 6

# Pins for the ultrasonic sensors (the number refers to the parking lot number).
TRIG_PIN1 = 11
ECHO_PIN1 = 13
TRIG_PIN2 = 9
ECHO_PIN2 = 10
TRIG_PIN3 = 7
ECHO_PIN3 = 12
TRIG_PIN4 = 8
ECHO_PIN4 = 14
TRIG_PIN5 = 15
ECHO_PIN5 = 16
TRIG_PIN6 = 17
ECHO_PIN16 = 18

PULSE_FREQUENCY = 50

GARAGE_ID = 1

##################
# Setting states #
##################
# The states are an array of length 3. This prevents false positives. Only when the sensor
# detects a car (or no car) for three consecutive the car will be detected. The first element
# indicates most recent measurement.
sensor1_state = [False] * 3
sensor2_state = [False] * 3
sensor3_state = [False] * 3
sensor4_state = [False] * 3
sensor5_state = [False] * 3
sensor6_state = [False] * 3


def setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    import led_control
    from entrance_system import udms_control

    setup_board()
    for i in range(1, 7):
        udms_control.setup_udms(eval(f"TRIG_PIN{i}"), eval(f"ECHO_PIN{i}"), i)
    logger.info("Setup of parking lot system completed successfully.")

    while True:
        for i in range(1, 7):
            led_control.update_led(
                udms_control.make_request(
                    udms_control.update_state(
                        udms_control.calculate_distance(
                            eval(f"TRIG_PIN{i}"), eval(f"ECHO_PIN{i}"), 1
                        ),
                        eval(f"sensor{i}_state"),
                        i,
                        GARAGE_ID,
                    )
                ),
                eval(f"PARKING{i}_LED"),
                i,
            )

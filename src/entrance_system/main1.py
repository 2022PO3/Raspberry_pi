import RPi.GPIO as GPIO
import logging
import sys
from entrance_system.udms_control import setup_udms, calculate_distance, take_picture
from entrance_system.servo_control import setup_servo

#################
# Logger config #
#################
def get_logger(name: str) -> logging.Logger:
    log_format = "%(asctime)s: %(message)s (%(name)8s)"
    logging.basicConfig(
        level=logging.INFO, format=log_format, filename="rpi_garage.log", filemode="w"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    logging.getLogger(name).addHandler(logging.StreamHandler(sys.stdout))
    return logging.getLogger(name)


logger = get_logger("rpi_garage")

#####################
# Defining the pins #
#####################
# Ultrasonic Sensor 1 on the entrance of the garage.
ECHO_PIN1 = 11
TRIG_PIN1 = 7
# Servo motor entrance.
SERVO_PIN1 = 13
# Pulse frequency of the PWM-pins.
PULSE_FREQUENCY = 50

##################
# Setting states #
##################
sensor1_state = False


def setup_board() -> None:
    # Use pin numbers.
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    setup_board()
    setup_udms(ECHO_PIN1, TRIG_PIN1, 1)
    servo1 = setup_servo(SERVO_PIN1, PULSE_FREQUENCY)
    logger.info("Setup of subsystem 1 completed successfully.")

    while True:
        sensor1_state = take_picture(
            calculate_distance(TRIG_PIN1, ECHO_PIN1, 1), sensor1_state, 1, servo1
        )

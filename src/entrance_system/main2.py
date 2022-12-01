import RPi.GPIO as GPIO
import logging
import sys
from udms_control import setup_udms, calculate_distance, take_picture
from servo_control import setup_servo

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


logger = get_logger("exit_system")

#####################
# Defining the pins #
#####################
# Ultrasonic Sensor 2 on th exit of the garage.
ECHO_PIN2 = 5
TRIG_PIN2 = 3
# Servo motor exit.
SERVO_PIN2 = 14
# Pulse frequency of the PWM-pins.
PULSE_FREQUENCY = 50

##################
# Setting states #
##################
sensor2_state = False


def setup_board() -> None:
    # Use pin numbers.
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    setup_board()
    setup_udms(ECHO_PIN2, TRIG_PIN2, 2)
    servo2 = setup_servo(SERVO_PIN2, PULSE_FREQUENCY)
    logger.info("Setup of exit system completed successfully.")
    try:
        while True:
            sensor2_state = take_picture(
                calculate_distance(TRIG_PIN2, ECHO_PIN2, 1), sensor2_state, 2, servo2
            )
    except KeyboardInterrupt:
        GPIO.cleanup()

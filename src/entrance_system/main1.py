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


logger = get_logger("entrance_system")

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
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


if __name__ == "__main__":
    import udms_control
    import servo_control

    setup_board()
    udms_control.setup_udms(TRIG_PIN1, ECHO_PIN1, 1)
    servo1 = servo_control.setup_servo(SERVO_PIN1, PULSE_FREQUENCY)
    logger.info("Setup of entrance system completed successfully.")

    while True:
        sensor1_state = udms_control.take_picture(
            udms_control.calculate_distance(TRIG_PIN1, ECHO_PIN1, 1),
            sensor1_state,
            1,
            servo1,
            servo_no=1,
        )

import logging
import sys
from udms_control import setup_udms, calculate_distance, take_picture

#################
# Logger config #
#################
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename="anpr_garage.log",
    filemode="w",
)
logger = logging.getLogger("anpr_garage")
logger.addHandler(logging.StreamHandler(sys.stdout))

#####################
# Defining the pins #
#####################
# Ultrasonic Sensor 1 on the entrance of the garage.
ECHO_PIN1 = 11
TRIG_PIN1 = 7
# Ultrasonic Sensor 2 on th exit of the garage.
ECHO_PIN2 = 5
TRIG_PIN2 = 3
# Servo motor entrance.
SERVO_PIN1 = 13
# Servo motor exit.
SERVO_PIN2 = 14
# Pins for 7-segment display
DISPLAY_PINS = [15, 16, 17, 18, 19, 20, 21]
# Pins for the LEDs.
PARKING1 = 1
PARKING2 = 2
PARKING3 = 3
PARKING4 = 4
PARKING5 = 5
PARKING6 = 6


if __name__ == "__main__":
    pass

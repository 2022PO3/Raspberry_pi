import RPi.GPIO as GPIO
from logger import get_logger

logger = get_logger("entrance_system")

# Pulse frequency of the PWM-pins.
PULSE_FREQUENCY = 50

##################
# Setting states #
##################
sensor_state = False


def _setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


def run_entrance_system(
    trig_pin: int, echo_pin: int, servo_pin: int, *, system: str
) -> None:
    import udms_control
    import servo_control

    _setup_board()
    udms_control.setup_udms(trig_pin, echo_pin, 1)
    servo = servo_control.setup_servo(servo_pin, PULSE_FREQUENCY)
    logger.info("Setup of entrance system completed successfully.")
    try:
        while True:
            sensor_state = udms_control.take_picture(
                udms_control.calculate_distance(trig_pin, echo_pin, 1),
                sensor_state,
                servo,
                system=system,
            )
    except KeyboardInterrupt:
        GPIO.cleanup()

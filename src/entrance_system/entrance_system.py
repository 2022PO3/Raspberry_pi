import RPi.GPIO as GPIO
from logger import get_logger, justify_logs
from time import sleep

logger = get_logger("entrance_system")

# Pulse frequency of the PWM-pins.
PULSE_FREQUENCY = 50


def _setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info(justify_logs("Setup of board completed.", 44))


def run_entrance_system(
    trig_pin: int, echo_pin: int, servo_pin: int, *, system: str
) -> None:
    import udms_control
    import servo_control

    _setup_board()
    sensor_state = False
    servo_state = False
    udms_control.setup_udms(trig_pin, echo_pin, system=system)
    servo = servo_control.setup_servo(servo_pin, PULSE_FREQUENCY)
    logger.info(justify_logs("Setup of entrance system completed.", 44))
    try:
        while True:
            sensor_state, servo_state = udms_control.take_picture(
                udms_control.calculate_distance(trig_pin, echo_pin, 1),
                sensor_state,
                servo,
                servo_state,
                system=system,
            )
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

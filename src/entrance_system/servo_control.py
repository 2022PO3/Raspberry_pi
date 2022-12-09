import RPi.GPIO as GPIO
from logger import get_logger, justify_logs
from time import sleep

logger = get_logger("servo_control")


class Servo:
    def ChangeDutyCycle(self, amount: int) -> None:
        ...


def setup_servo(servo_pin: int, pulse_frequency: int) -> Servo:
    GPIO.setup(servo_pin, GPIO.OUT)
    logger.info(justify_logs(f"Setup of servo on pin {servo_pin} completed.", 44))
    servo = GPIO.PWM(servo_pin, pulse_frequency)
    servo.start(0)
    servo.ChangeDutyCycle(0)
    sleep(1)
    return servo


def open_barrier(servo: Servo, servo_state: bool, *, system: str) -> bool:
    if not servo_state:
        servo.ChangeDutyCycle(12)
        sleep(1)
        servo.ChangeDutyCycle(0)
        logger.info(justify_logs(f"Opened barrier of {system}.", 44))
    return not servo_state


def close_barrier(servo: Servo, servo_state: bool, *, system: str) -> bool:
    if servo_state:
        servo.ChangeDutyCycle(7)
        sleep(1)
        servo.ChangeDutyCycle(0)
        logger.info(justify_logs(f"Closed barrier of {system}.", 44))
    return not servo_state

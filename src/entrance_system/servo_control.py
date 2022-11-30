import RPi.GPIO as GPIO
import main1
from time import sleep

logger = main1.get_logger("servo_control")


def setup_servo(servo_pin: int, pulse_frequency: int):
    GPIO.setup(servo_pin, GPIO.OUT)
    logger.info(f"Setup of servo on pin {servo_pin} completed.")
    servo = GPIO.PWM(servo_pin, pulse_frequency)
    servo.start(0)
    servo.ChangeDutyCycle(7)
    sleep(1)
    return servo


def open_barrier(servo, servo_no: int) -> None:
    servo.ChangeDutyCycle(12)
    sleep(1)
    logger.info(f"Opened barrier of servo {servo_no}.")


def close_barrier(servo, servo_no: int) -> None:
    servo.ChangeDutyCycle(7)
    sleep(1)
    logger.info(f"Closed barrier of servo {servo_no}.")

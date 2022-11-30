import RPi.GPIO as GPIO
import main1

logger = main1.get_logger("servo_control")


def setup_servo(servo_pin: int, pulse_frequency: int):
    GPIO.setup(servo_pin, GPIO.OUT)
    logger.info(f"Setup of servo on pin {servo_pin} completed.")
    servo = GPIO.PWM(servo_pin, pulse_frequency)
    servo.start(2.5)
    return servo


def _set_angle(angle: int, servo, servo_no: int) -> None:
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)


def open_barrier(servo, servo_no: int) -> None:
    _set_angle(90, servo, servo_no)
    logger.info(f"Opened barrier of servo {servo_no}.")


def close_barrier(servo, servo_no: int) -> None:
    _set_angle(0, servo, servo_no)
    logger.info(f"Closed barrier of servo {servo_no}.")

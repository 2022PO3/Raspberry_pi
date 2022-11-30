import RPi.GPIO as GPIO
import main1

logger = main1.get_logger("servo_control")


def setup_servo(servo_pin: int, pulse_frequency: int):
    GPIO.setup(servo_pin, GPIO.OUT)
    logger.info(f"Setup of servo on pin {servo_pin} completed.")
    return GPIO.PWM(servo_pin, pulse_frequency)


def _set_angle(angle: int, servo, servo_no: int) -> None:
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    logger.info(f"Set servo {servo_no} to {angle} degrees.")


def open_barrier(servo, servo_no: int) -> None:
    _set_angle(90, servo, servo_no)
    logger.info(f"Opened barrier of servo {servo_no}.")


def close_barrier(servo, servo_no: int) -> None:
    _set_angle(0, servo, servo_no)
    logger.info(f"Closed barrier of servo {servo_no}.")

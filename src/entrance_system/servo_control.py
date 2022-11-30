import RPi.GPIO as GPIO
import entrance_system.main1 as main1

logger = main1.get_logger("rpi_garage")


def setup_servo(servo_pin: int, pulse_frequency: int):
    GPIO.setup(servo_pin, GPIO.OUT)
    logger.info(f"Setup of servo on pin {servo_pin} completed.")
    return GPIO.PWM(servo_pin, pulse_frequency)


def _set_angle(angle: int, servo) -> None:
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    logger.info(f"Set {servo} to {angle} degrees.")


def open_barrier(servo) -> None:
    _set_angle(90, servo)
    logger.info(f"Opened barrier of {servo}.")


def close_barrier(servo) -> None:
    _set_angle(0, servo)
    logger.info(f"Closed barrier of {servo}.")

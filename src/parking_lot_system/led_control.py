import RPi.GPIO as GPIO
import main

logger = main.get_logger("led_control")


def setup_led(pin_no: int) -> None:
    GPIO.setup(pin_no, GPIO.OUT)
    GPIO.output(pin_no, GPIO.LOW)
    logger.info(f"Setup of LEDs on pin {pin_no} completed.")


def turn_on_green(pin_no: int, parking_no: int) -> None:
    GPIO.output(pin_no, GPIO.LOW)
    logger.info(f"Turned on green LED in parking {parking_no}")


def turn_on_red(pin_no: int, parking_no: int) -> None:
    GPIO.output(pin_no, GPIO.HIGH)
    logger.info(f"Turned on red LED in parking {parking_no}")

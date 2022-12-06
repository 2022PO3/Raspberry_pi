import RPi.GPIO as GPIO
from logger import get_logger

logger = get_logger("led_control")


def setup_led(pin_tuple: tuple[int, int], parking_no: int) -> None:
    red_pin, green_pin = pin_tuple
    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.setup(green_pin, GPIO.OUT)
    GPIO.output(green_pin, GPIO.LOW)
    logger.info(f"Setup of LEDs of parking {parking_no} completed.")


def turn_on_red(pin_tuple: tuple[int, int], parking_no: int) -> None:
    red_pin, green_pin = pin_tuple
    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.LOW)
    logger.info(f"Turned on LED in parking {parking_no}.")


def turn_on_green(pin_tuple: tuple[int, int], parking_no: int) -> None:
    red_pin, green_pin = pin_tuple
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.HIGH)
    logger.info(f"Turned off LED in parking {parking_no}.")

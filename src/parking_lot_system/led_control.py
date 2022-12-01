import RPi.GPIO as GPIO
import main

logger = main.get_logger("led_control")


def setup_led(pin_no: int) -> None:
    GPIO.setup(pin_no, GPIO.OUT)
    logger.info(f"Setup of LEDs on pin {pin_no} completed.")


def update_led(sensor_state: list[bool], pin_no: int, parking_no: int) -> None:
    if sensor_state == [True] * 3:
        _turn_on_red(pin_no, parking_no)
    elif sensor_state == [False] * 3:
        _turn_on_green(pin_no, parking_no)


def _turn_on_green(pin_no: int, parking_no: int) -> None:
    GPIO.output(pin_no, GPIO.HIGH)
    logger.info(f"Turned on green LED in parking {parking_no}")


def _turn_on_red(pin_no: int, parking_no: int) -> None:
    GPIO.output(pin_no, GPIO.HIGH)
    logger.info(f"Turned on red LED in parking {parking_no}")

import RPi.GPIO as GPIO
import parking_lot_system.main_pi1 as main_pi1

logger = main_pi1.get_logger("led_control")


def setup_led(pin_no: int) -> None:
    GPIO.setup(pin_no, GPIO.OUT)
    GPIO.output(pin_no, GPIO.LOW)
    logger.info(f"Setup of LEDs on pin {pin_no} completed.")


def turn_on(pin_no: int, parking_no: int) -> None:
    GPIO.output(pin_no, GPIO.HIGH)
    logger.info(f"Turned on LED in parking {parking_no}.")


def turn_off(pin_no: int, parking_no: int) -> None:
    GPIO.output(pin_no, GPIO.LOW)
    logger.info(f"Turned off LED in parking {parking_no}.")

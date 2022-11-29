import RPi.GPIO as GPIO
import time


#define pins [pinA, pinB, pinC, pinD, pinE, pinF, pinG]
led_pins = [1, 2, 3, 4, 5, 6]

def setup_leds():
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)


# functions turn on green leds
def turn_on_green(pin_no: int) -> None:
    GPIO.output(pin_no, GPIO.HIGH)


# turn on red leds
def turn_on_red(pin_no: int) -> None:
    GPIO.output(pin_no, GPIO.HIGH)


# turn off green leds
def turn_off_green(pin_no: int) -> None:
    GPIO.output(pin_no, GPIO.LOW)


def turn_off_red(pin_no: int) -> None:
    GPIO.output(pin_no, GPIO.LOW)


def change_leds(availeble: list):
    """

    Args:
        availeble:  list with bool, true if spot is occupied

    Returns: None

    """
    for i in range(len(availeble)):
        if availeble[i]:
            turn_on_red(led_pins[i])
            turn_off_green(led_pins[i])
            time.sleep(0.5)
        else:
            turn_off_red(led_pins[i])
            turn_on_green(led_pins[i])
            time.sleep(0.5)

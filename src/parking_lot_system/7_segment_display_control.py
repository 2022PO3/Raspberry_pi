import RPi.GPIO as GPIO
import time


parking1_detected = True
parking2_detected = True
parking3_detected = True
parking4_detected = True
parking5_detected = True
parking6_detected = True

NUMBER_OF_SPACES = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# define pins [pinA, pinB, pinC, pinD, pinE, pinF, pinG]
PINS = [15, 16, 17, 18, 19, 20, 21]

# Setup
def setup_display(pins: list[int]) -> None:
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)


# define 7 segment digits
high = 0
low = 1

digitclr = [low, low, low, low, low, low, low]
digit0 = [high, high, high, high, high, low]
digit1 = [low, high, high, low, low, low, low]
digit2 = [high, high, low, high, high, low, high]
digit3 = [high, high, high, high, low, low, high]
digit4 = [low, high, high, low, low, high, high]
digit5 = [high, low, high, high, low, high, high]
digit6 = [high, low, high, high, high, high, high]
digit7 = [high, high, high, low, low, low, low]
digit8 = [high, high, high, high, high, high, high]
digit9 = [high, high, high, high, low, high, high]


def reset() -> None:
    for x in range(7):
        GPIO.output(PINS[x], digitclr[x])
        time.sleep(0.1)


def print_digit(digit: list) -> None:
    reset()
    for x in range(7):
        GPIO.output(PINS[x], digit[x])


def free_spots() -> int:
    """
    Returns the number of free spots in the garage.
    """
    aantal_bezet = 0
    if parking1_detected:
        aantal_bezet += 1
    if parking2_detected:
        aantal_bezet += 1
    if parking3_detected:
        aantal_bezet += 1
    if parking4_detected:
        aantal_bezet += 1
    if parking5_detected:
        aantal_bezet += 1
    if parking6_detected:
        aantal_bezet += 1
    return NUMBER_OF_SPACES - aantal_bezet


def print_spots() -> None:
    """
    Prints the correct number of spots on the 7-segment display.
    """
    digit = free_spots()
    if digit == 1:
        print_digit(digit1)
    elif digit == 2:
        print_digit(digit2)
    elif digit == 3:
        print_digit(digit3)
    elif digit == 4:
        print_digit(digit4)
    elif digit == 5:
        print_digit(digit5)
    elif digit == 6:
        print_digit(digit6)

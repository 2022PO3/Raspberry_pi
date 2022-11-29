import RPi.GPIO as GPIO
import time


#define pins [pinA, pinB, pinC, pinD, pinE, pinF, pinG]
display_pins = [15, 16, 17, 18, 19, 20, 21]

#define 7 segment digits
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

digits = (digit0, digit1, digit2, digit3, digit4, digit5, digit6, digit7, digit8, digit9, digitclr)


def setup_display():
    for pin in display_pins:
        GPIO.setup(pin, GPIO.OUT)


def reset_display():
    for x in range(0,7):
        GPIO.output(display_pins[x], digitclr[x])
        time.sleep(0.1)


def prntdigit(digit):
    reset()
    for x in range(0,7):
        GPIO.output(display_pins[x], digit[x])


def aantal_vrij(available_spots: list):
    aantal_bezet = 0
    for parking in available_spots:
        if parking[1]:
            available_spots += 1
    return 6 - aantal_bezet


def change_display(available_spots: list):
    """

    Args:
        available_spots: list with bool, true if spot is occupied

    Returns: None

    """
    free_spots = aantal_vrij(available_spots)
    prntdigit(digits[free_spots + 1])




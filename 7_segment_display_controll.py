import RPi.GPIO as GPIO
import time


parking1_detected = True
parking2_detected = True
parking3_detected = True
parking4_detected = True
parking5_detected = True
parking6_detected = True

number_of_spaces = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#define pins [pinA, pinB, pinC, pinD, pinE, pinF, pinG]
pins = [15, 16, 17, 18, 19, 20, 21]

#setup
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

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

def reset():
    for x in range(0,7):
        GPIO.output(pins[x], digitclr[x])
        time.sleep(0.1)

def prntdigit(digit):
    reset()
    for x in range(0,7):
        GPIO.output(pins[x], digit[x])

def aantal_vrij():
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
    return number_of_spaces - aantal_bezet


digit = aantal_vrij()
if digit == 1:
    prntdigit(digit1)
elif digit == 2:
    prntdigit(digit2)
elif digit == 3:
    prntdigit(digit3)
elif digit == 4:
    prntdigit(digit4)
elif digit == 5:
    prntdigit(digit5)
elif digit == 6:
    prntdigit(digit6)




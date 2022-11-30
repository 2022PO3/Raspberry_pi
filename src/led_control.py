import RPi.GPIO as GPIO
import time

parking1_detected = True
parking2_detected = True
parking3_detected = True
parking4_detected = True
parking5_detected = True
parking6_detected = True


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# define pins
parking1 = 1
parking2 = 2
parking3 = 3
parking4 = 4
parking5 = 5
parking6 = 6

parkings_detected = [(parking1_detected, parking1),
                     (parking2_detected, parking2),
                     (parking3_detected, parking3),
                     (parking4_detected, parking4),
                     (parking5_detected, parking5),
                     (parking6_detected, parking6)]

# setup
GPIO.setup(parking1, GPIO.OUT)
GPIO.setup(parking2, GPIO.OUT)
GPIO.setup(parking3, GPIO.OUT)
GPIO.setup(parking4, GPIO.OUT)
GPIO.setup(parking5, GPIO.OUT)
GPIO.setup(parking6, GPIO.OUT)


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


for parking in parkings_detected:
    if parking[1]:
        turn_on_red(parking[2])
        turn_off_green(parking[2])
        time.sleep(0.5)
    else:
        turn_off_red(parking[2])
        turn_on_green(parking[2])
        time.sleep(0.5)



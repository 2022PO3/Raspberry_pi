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
parking1green = 1
parking1red = 2
parking2green = 3
parking2red = 4
parking3green = 5
parking3red = 6
parking4green = 7
parking4red = 8
parking5green = 9
parking5red = 10
parking6green = 11
parking6red = 12

# setup
GPIO.setup(parking1green, GPIO.OUT)
GPIO.setup(parking1red, GPIO.OUT)
GPIO.setup(parking2green, GPIO.OUT)
GPIO.setup(parking2red, GPIO.OUT)
GPIO.setup(parking3green, GPIO.OUT)
GPIO.setup(parking3red, GPIO.OUT)
GPIO.setup(parking4green, GPIO.OUT)
GPIO.setup(parking4red, GPIO.OUT)
GPIO.setup(parking5green, GPIO.OUT)
GPIO.setup(parking5red, GPIO.OUT)
GPIO.setup(parking6green, GPIO.OUT)
GPIO.setup(parking6red, GPIO.OUT)


# functions turn on green leds
def turn_on_parking1green():
    GPIO.output(parking1green, GPIO.HIGH)


def turn_on_parking2green():
    GPIO.output(parking2green, GPIO.HIGH)


def turn_on_parking3green():
    GPIO.output(parking3green, GPIO.HIGH)


def turn_on_parking4green():
    GPIO.output(parking4green, GPIO.HIGH)


def turn_on_parking5green():
    GPIO.output(parking5green, GPIO.HIGH)


def turn_on_parking6green():
    GPIO.output(parking6green, GPIO.HIGH)


# turn on red leds
def turn_on_parking1red():
    GPIO.output(parking1red, GPIO.HIGH)


def turn_on_parking2red():
    GPIO.output(parking2red, GPIO.HIGH)


def turn_on_parking3red():
    GPIO.output(parking3red, GPIO.HIGH)


def turn_on_parking4red():
    GPIO.output(parking4red, GPIO.HIGH)


def turn_on_parking5red():
    GPIO.output(parking5red, GPIO.HIGH)


def turn_on_parking6red():
    GPIO.output(parking6red, GPIO.HIGH)


# turn off green leds
def turn_off_parking1green():
    GPIO.output(parking1green, GPIO.LOW)


def turn_off_parking2green():
    GPIO.output(parking2green, GPIO.LOW)


def turn_off_parking3green():
    GPIO.output(parking3green, GPIO.LOW)


def turn_off_parking4green():
    GPIO.output(parking4green, GPIO.LOW)


def turn_off_parking5green():
    GPIO.output(parking5green, GPIO.LOW)


def turn_off_parking6green():
    GPIO.output(parking6green, GPIO.LOW)


# turn off red leds
def turn_off_parking1red():
    GPIO.output(parking1red, GPIO.LOW)


def turn_off_parking2red():
    GPIO.output(parking2red, GPIO.LOW)


def turn_off_parking3red():
    GPIO.output(parking3red, GPIO.LOW)


def turn_off_parking4red():
    GPIO.output(parking4red, GPIO.LOW)


def turn_off_parking5red():
    GPIO.output(parking5red, GPIO.LOW)


def turn_off_parking6red():
    GPIO.output(parking6red, GPIO.LOW)


if parking1_detected:
    turn_off_parking1red()
    time.sleep(0.5)
    turn_on_parking1green()
    time.sleep(0.5)

else:
    turn_off_parking1green()
    time.sleep(0.5)
    turn_on_parking1red()
    time.sleep(0.5)

if parking2_detected:
    turn_off_parking2red()
    time.sleep(0.5)
    turn_on_parking2green()
    time.sleep(0.5)

else:
    turn_off_parking2green()
    time.sleep(0.5)
    turn_on_parking2red()
    time.sleep(0.5)

if parking3_detected:
    turn_off_parking3red()
    time.sleep(0.5)
    turn_on_parking3green()
    time.sleep(0.5)

else:
    turn_off_parking3green()
    time.sleep(0.5)
    turn_on_parking3red()
    time.sleep(0.5)

if parking4_detected:
    turn_off_parking4red()
    time.sleep(0.5)
    turn_on_parking4green()
    time.sleep(0.5)

else:
    turn_off_parking4green()
    time.sleep(0.5)
    turn_on_parking4red()
    time.sleep(0.5)

if parking5_detected:
    turn_off_parking5red()
    time.sleep(0.5)
    turn_on_parking5green()
    time.sleep(0.5)

else:
    turn_off_parking5green()
    time.sleep(0.5)
    turn_on_parking5red()
    time.sleep(0.5)

if parking6_detected:
    turn_off_parking6red()
    time.sleep(0.5)
    turn_on_parking6green()
    time.sleep(0.5)

else:
    turn_off_parking6green()
    time.sleep(0.5)
    turn_on_parking6red()
    time.sleep(0.5)

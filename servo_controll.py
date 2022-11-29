import RPi.GPIO as GPIO
import time

number_plate_detected_entering = True
number_plate_detected_leaving = True
auto_detected_entering = True
auto_detected_leaving = True

servoPIN1 = 13
servoPIN2 = 14
pulse_frequency = 50
GPIO.setmode(GPIO.BOARD) #we use pin numbers
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)

servo1 = GPIO.PWM(servoPIN1, pulse_frequency)
servo2 = GPIO.PWM(servoPIN2, pulse_frequency)

def setAngle(angle, servo):
    duty = angle/18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(1)

if number_plate_detected_entering:
    setAngle(90, servo1)
    while auto_detected_entering:
        time.sleep(1)
    setAngle(0, servo1)

if number_plate_detected_leaving:
    setAngle(90, servo2)
    while not auto_detected_leaving:
        time.sleep(1)
    setAngle(0, servo2)




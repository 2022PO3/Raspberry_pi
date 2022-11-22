import RPi.GPIO as GPIO
import time


def setup_udms(trig_pin: int, echo_pin: int) -> None:
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    print("Waiting for sensor to settle")

    time.sleep(2)


def calculate_distance(trig_pin: int, echo_pin: int, time_delta: int) -> None:
    GPIO.output(trig_pin, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(trig_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    distance = round(pulse_duration * 17150, 2)

    print("Distance:", distance, "cm")
    time.sleep(time_delta)


if __name__ == "__main__":
    ECHO_PIN = 11
    TRIG_PIN = 7
    setup_udms(TRIG_PIN, ECHO_PIN)
    while True:
        calculate_distance(TRIG_PIN, ECHO_PIN, 1)

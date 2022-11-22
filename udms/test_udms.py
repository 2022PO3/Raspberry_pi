import logging
import RPi.GPIO as GPIO
import time

# Config of the logger for logging entrances and exits of the garage.
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename="anpr_garage.log",
    filemode="w",
)


def setup_udms(trig_pin: int, echo_pin: int) -> None:
    """
    Sets up the udms on the `trig_pin` and `echo_pin`.
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    print("Waiting for sensor to settle")

    time.sleep(2)


def calculate_distance(trig_pin: int, echo_pin: int, time_delta: int) -> float:
    """
    Reads on the distance measuring of the udms connected on the `trig_pin` and `echo_pin`.
    """
    time.sleep(time_delta)

    GPIO.output(trig_pin, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(trig_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    return round(pulse_duration * 17150, 2)


def take_picture(distance: float, sensor_no: int) -> None:
    """
    Takes picture when the distance is small enough (car is on top of the sensor).
    """
    print(f"Sensor {sensor_no} distance: {distance}.")
    if distance < 3:
        logging.info("Sensor {sensor_no} detected a car!")


if __name__ == "__main__":
    ECHO_PIN1 = 11
    TRIG_PIN1 = 7
    ECHO_PIN2 = 5
    TRIG_PIN2 = 3
    setup_udms(TRIG_PIN1, ECHO_PIN1)
    setup_udms(TRIG_PIN2, ECHO_PIN2)
    while True:
        take_picture(calculate_distance(TRIG_PIN1, ECHO_PIN1, 1), 1)
        take_picture(calculate_distance(TRIG_PIN2, ECHO_PIN2, 1), 2)

import RPi.GPIO as GPIO
import time
import main
import requests
import json
import os

logger = main.get_logger("display_control")

####################
# Define constants #
####################

GARAGE_ID = 11

# Define pins [pinA, pinB, pinC, pinD, pinE, pinF, pinG]
PINS = [40, 38, 37, 36, 35, 33, 31]

# Define 7 segment digits
HIGH = 0
LOW = 1

DIGITS = {
    -1: [LOW, LOW, LOW, LOW, LOW, LOW, LOW],
    0: [HIGH, HIGH, HIGH, HIGH, HIGH, LOW],
    1: [LOW, HIGH, HIGH, LOW, LOW, LOW, LOW],
    2: [HIGH, HIGH, LOW, HIGH, HIGH, LOW, HIGH],
    3: [HIGH, HIGH, HIGH, HIGH, LOW, LOW, HIGH],
    4: [HIGH, LOW, HIGH, HIGH, LOW, HIGH, HIGH],
    5: [HIGH, LOW, HIGH, HIGH, LOW, HIGH, HIGH],
    6: [HIGH, LOW, HIGH, HIGH, HIGH, HIGH, HIGH],
}

##################
# Main functions #
##################


def setup_board() -> None:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


def setup_display(pins: list[int]) -> None:
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
    logger.info("Setup of screen completed.")


def reset() -> None:
    for x in range(7):
        GPIO.output(PINS[x], DIGITS[-1][x])
        time.sleep(0.1)


def print_digit(digit: int) -> None:
    reset()
    for x in range(7):
        GPIO.output(PINS[x], DIGITS[digit][x])
    logger.info(f"Printed digit {digit} on screen.")


def get_free_spots() -> int:
    url = f"https://po3backend.ddns.net/api/garage/{GARAGE_ID}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = json.loads(requests.get(url, headers=headers).text)
    return int(response["data"]["unoccupiedLots"])


if __name__ == "__main__":
    setup_board()
    try:
        while True:
            print_digit(get_free_spots())
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()

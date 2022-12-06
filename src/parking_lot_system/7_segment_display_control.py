import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import time
import requests
import json
import os

from logger import get_logger
from PIL import ImageFont


logger = get_logger("display_control")

####################
# Define constants #
####################

GARAGE_ID = 11

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000


# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# Define pins [pinA, pinB, pinC, pinD, pinE, pinF, pinG]
PINS = [40, 38, 37, 36, 35, 33, 31]

##################
# Main functions #
##################


def setup_board() -> None:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info("Setup of board completed.")


def setup_display() -> TFT.ST7735:
    # Create TFT LCD display class.
    disp = TFT.ST7735(
        DC,
        rst=RST,
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPEED_HZ),
    )
    disp.begin()
    disp.clear((255, 0, 0))
    logger.info("Setup of screen completed.")
    return disp


def write(inst: TFT.ST7735, string: str) -> None:
    font = ImageFont.load_default(size=15)
    inst.text((10, 10), string, font=font, fill=(255, 255, 255))


def reset(inst: TFT.ST7735) -> None:
    inst.reset()


def get_free_spots() -> int:
    url = f"https://po3backend.ddns.net/api/garage/{GARAGE_ID}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = json.loads(requests.get(url, headers=headers).text)
    return int(response["data"]["unoccupiedLots"])


if __name__ == "__main__":
    setup_board()
    disp = setup_display()
    try:
        while True:
            left_spots = get_free_spots()
            print(left_spots)
            write(disp, f"{left_spots}/6")
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()

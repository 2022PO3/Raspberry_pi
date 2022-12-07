import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import time
import requests
import json
import os
import socket

from typing import Any
from logger import get_logger, justify_logs
from PIL import ImageFont
from PIL import Image


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

###################
# Type definition #
###################
class GarageInfo:
    def __init__(self, name: str, total_spots: int, left_spots: int) -> None:
        self.name = name
        self.total_spots = total_spots
        self.left_spots = left_spots

    @classmethod
    def fromJSON(cls, json: dict[str, Any]) -> "GarageInfo":
        return GarageInfo(
            json["data"]["name"],
            json["data"]["parkingLots"],
            json["data"]["unoccupiedLots"],
        )


##################
# Main functions #
##################
def setup_display() -> TFT.ST7735:
    # Create TFT LCD display class.
    disp = TFT.ST7735(
        DC,
        rst=RST,
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPEED_HZ),
    )
    disp.begin()
    disp.clear((255, 255, 255))
    logger.info(justify_logs("Setup of screen completed."))
    return disp


def write(inst: TFT.ST7735, string: str, *, font_size: int, x: int, y: int) -> None:
    font = ImageFont.truetype(
        "src/parking_lot_system/fonts/OpenSans-Bold.ttf", size=font_size
    )
    draw = inst.draw()
    draw.text((x, y), string, font=font, fill=(0, 0, 0))
    inst.display()


def reset(inst: TFT.ST7735) -> None:
    inst.reset()


def get_free_spots() -> GarageInfo:
    url = f"https://po3backend.ddns.net/api/garage/{GARAGE_ID}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = json.loads(requests.get(url, headers=headers).text)
    return GarageInfo.fromJSON(response)


if __name__ == "__main__":
    disp = setup_display()
    try:
        while True:
            garage_info = get_free_spots()
            disp.clear((255, 255, 255))
            image = Image.open("src/parking_lot_system/logo_parking_boys.png")
            write(
                disp,
                f"{garage_info.left_spots}/{garage_info.total_spots}",
                font_size=65,
                x=14,
                y=60,
            )
            disp.display(image.resize((WIDTH, int(HEIGHT / 4))))
            logger.info(justify_logs("Written output to screen."))
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()

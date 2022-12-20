import ST7735 as TFT  # type: ignore
import Adafruit_GPIO.SPI as SPI  # type: ignore
import RPi.GPIO as GPIO
import time

from dotenv import load_dotenv
from garage import get_free_spots
from typing import Any
from logger import get_logger, justify_logs
from PIL import ImageFont
from PIL import Image


logger = get_logger("display_control")
load_dotenv()

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
        print(json)
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
    logger.info(justify_logs("Setup of screen completed.", 44))
    return disp


def write(inst: TFT.ST7735, string: str, *, font_size: int, x: int, y: int) -> None:
    font = ImageFont.truetype(
        "src/parking_lot_system/fonts/OpenSans-Bold.ttf", size=font_size
    )
    draw = inst.draw()
    draw.text((x, y), string, font=font, fill=(0, 0, 0))
    inst.display()


if __name__ == "__main__":
    disp = setup_display()
    try:
        while True:
            try:
                garage_info = get_free_spots(GARAGE_ID)
            except Exception as e:
                logger.error(f"Some error occurred: {e}.")
                raise e
            disp.clear((255, 255, 255))
            image = Image.open("src/parking_lot_system/logo_parking_boys.png")
            try:
                write(
                    disp,
                    f"{garage_info.left_spots}/{garage_info.total_spots}",
                    font_size=65,
                    x=14,
                    y=60,
                )
            except UnboundLocalError:
                pass
            disp.display(image.resize((WIDTH, int(HEIGHT / 4))))
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()

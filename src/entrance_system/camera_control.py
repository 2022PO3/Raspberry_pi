import io
import os
import re

from logger import get_logger, log
from picamera import PiCamera
from google.cloud import vision


logger = get_logger("camera_control")


def setup_google() -> vision.ImageAnnotatorClient:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.getcwd(), "google_vision_api_credentials.json"
    )
    return vision.ImageAnnotatorClient()


def take_image(path: str) -> None:
    camera = PiCamera(resolution=(320, 320), vflip=True, hflip=True)
    camera.resolution = (1024, 768)
    camera.capture(path)
    log("Image taken.", logger)


def get_text_from_image_path(path: str) -> str:
    """
    This method reads the text on the image at the given path, using Google Vision API.

    @param path: location the image is stored at. If this parameter is None, the default_image_path attribute of
    this class instance is used.
    """

    # Open the image
    with io.open(path, "rb") as image_file:
        content = image_file.read()

    # Send image to the Google Vision API
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return response.text_annotations[0].description


def filter_licence_plate(detected_licence_plate: str) -> str:
    licence_plate_text = re.sub(r"\W", "", detected_licence_plate)
    matches = re.findall(r"\d[A-Z]{3}\d{3}", licence_plate_text)
    if matches is not None:
        return matches[0]
    return ""


if __name__ == "__main__":
    client = setup_google()
    take_image("image.jpg")
    # detected_licence_plate_text = get_text_from_image_path(
    #    "/home/marcus/po3/Raspberry_pi/src/entrance_system/image.jpg"
    # )
# print(filter_licence_plate(detected_licence_plate_text))

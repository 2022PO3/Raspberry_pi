import os
import json
import requests

from logger import get_logger, log
from typing import Any

logger = get_logger("garage_control")


class Garage:
    def __init__(
        self,
        name: str,
        total_spots: int,
        entered: int,
        reservations: int,
    ) -> None:
        self.name = name
        self.total_spots = total_spots
        self.entered = entered
        self.reservations = reservations

    @classmethod
    def fromJSON(cls, json: dict[str, Any]) -> "Garage":
        return Garage(
            json["data"]["name"],
            len(json["data"]["parkingLots"]),
            int(json["data"]["entered"]),
            int(json["data"]["reservations"]),
        )


def get_free_spots(garage_id: int):
    url = f"{os.getenv('SERVER_URL')}api/rpi/garage/{garage_id}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                response_json = json.loads(requests.get(url, headers=headers).text)
                return Garage.fromJSON(response_json)
            except json.decoder.JSONDecodeError:
                log("Request returned an empty response.", logger)
        else:
            log(
                f"Request returned a non-200 status code: {response.status_code}.",
                logger,
            )
    except requests.exceptions.ConnectionError:
        log("Request failed. Retrying in 1 second.", logger)

    return None

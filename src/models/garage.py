import os
import json
import requests

from typing import Any


class Garage:
    def __init__(self, name: str, total_spots: int, free_spots: int) -> None:
        self.name = name
        self.total_spots = total_spots
        self.left_spots = free_spots

    @classmethod
    def fromJSON(cls, json: dict[str, Any]) -> "Garage":
        return Garage(
            json["data"]["name"],
            json["data"]["parkingLots"],
            json["data"]["unoccupiedLots"],
        )


def get_free_spots(garage_id: int) -> "Garage":
    url = f"https://po3backend.ddns.net/api/garage/{garage_id}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = json.loads(requests.get(url, headers=headers).text)
    return Garage.fromJSON(response)

import json
import requests
import os
from typing import Any
from datetime import datetime, timedelta
from dateparser import parse


class Reservation:
    def __init__(
        self,
        parking_lot_no: int,
        from_date: datetime,
        to_date: datetime,
    ) -> None:
        self.parking_lot_no = parking_lot_no
        self.from_date = from_date
        self.to_date = to_date

    def is_active(self) -> bool:
        """
        Returns whether this reservation is active or not.
        """
        return self.from_date - timedelta(hours=8) < datetime.now() < self.to_date

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> dict[int, "Reservation"]:
        parkingLotNo: int = json["parkingLot"]["parkingLotNo"]
        return {
            parkingLotNo: Reservation(
                json["parkingLot"]["parkingLotNo"],
                parse(json["from_date"]),
                parse(json["to_date"]),
            )
        }

    @classmethod
    def from_list_json(cls, json: dict[str, Any]) -> list[dict[int, "Reservation"]]:
        print(json)
        try:
            data = json["data"]
            return [
                Reservation.from_json(json_reservation) for json_reservation in data
            ]
        except KeyError:
            print(json["errors"])


def get_garage_reservations(garage_id: int) -> list[dict[int, "Reservation"]]:
    url = f"https://po3backend.ddns.net/api/rpi/reservations/{garage_id}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = json.loads(requests.get(url, headers=headers).text)
    return Reservation.from_list_json(response)

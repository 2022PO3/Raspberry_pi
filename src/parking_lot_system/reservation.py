import json
import requests
import os

from logger import get_logger, log
from typing import Any
from datetime import datetime, timedelta
from dateparser import parse

logger = get_logger("reservation_control")


class Reservation:
    def __init__(
        self,
        parking_lot_no: int,
        from_date: datetime,
        to_date: datetime,
        is_valid: bool,
    ) -> None:
        self.parking_lot_no = parking_lot_no
        self.from_date = from_date
        self.to_date = to_date
        self.is_valid = is_valid

    def is_active(self) -> bool:
        """
        Returns whether this reservation is active or not.
        """
        return (
            self.from_date - timedelta(hours=8)
            < datetime.now().astimezone()
            < self.to_date
        ) and self.is_valid

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> "Reservation":
        return Reservation(
            json["parkingLot"]["parkingLotNo"],
            parse(json["fromDate"]),  # type: ignore
            parse(json["toDate"]),  # type: ignore
            json["is_valid"],
        )

    @classmethod
    def from_list_json(cls, json: dict[str, Any]) -> dict[int, "Reservation"]:
        try:
            data = json["data"]
            reservation_dict: dict[int, Reservation] = dict()
            for json_reservation in data:
                r = Reservation.from_json(json_reservation)
                reservation_dict |= {r.parking_lot_no: r}
            return reservation_dict
        except KeyError:
            return dict()


def get_garage_reservations(garage_id: int) -> dict[int, "Reservation"]:
    url = f"{os.getenv('SERVER_URL')}api/rpi/reservations/{garage_id}"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            response_json = json.loads(requests.get(url, headers=headers).text)
        except json.decoder.JSONDecodeError:
            log("Request returned an empty response.", logger)
        return Reservation.from_list_json(response_json)
    else:
        log(f"Request returned a non-200 status code: {response.status_code}.", logger)
    return dict()

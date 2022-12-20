import time
import os
import requests
import led_control
import RPi.GPIO as GPIO
from logger import get_logger, justify_logs
import reservation

logger = get_logger("udms_control")


def setup_udms(pin_list: tuple[int, int], sensor_no: int) -> None:
    """
    Sets up the udms on the `trig_pin` and `echo_pin`.
    Pin list is of the format: `[TRIG_PIN, ECHO_PIN]`.
    """
    trig_pin, echo_pin = pin_list
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, GPIO.LOW)

    time.sleep(1)
    logger.info(justify_logs(f"Setup of ultrasonic sensor {sensor_no} completed.", 44))


def calculate_distance(pin_list: tuple[int, int], time_delta: int) -> float:
    """
    Reads on the distance measuring of the udms connected on the `trig_pin` and `echo_pin`.
    Pin list is of the format: `[TRIG_PIN, ECHO_PIN]`.
    """
    trig_pin, echo_pin = pin_list
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


######################
# Parking lot system #
######################
def update_parking_lot(
    sensor_state: list[bool],
    distance: float,
    led_pin_no: tuple[int, int],
    parking_no: int,
    garage_id: int,
    reservation_dict: dict[int, reservation.Reservation],
) -> list[bool]:
    """
    Makes request about the state of the parking lot to the Backend.
    """
    url = f"{os.getenv('SERVER_URL')}/api/rpi/parking-lot"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    body = {"garageId": garage_id, "parkingLotNo": parking_no}
    if parking_no in reservation_dict:
        p_lot_r = reservation_dict[parking_no]
        if p_lot_r.is_active():
            led_control.turn_on_red(led_pin_no, parking_no)
            logger.info(
                justify_logs(
                    f"Parking lot {parking_no} is booked on {p_lot_r.from_date}.", 44
                )
            )
            return [True, True]

    if distance < 5 and sensor_state == [True, False]:
        led_control.turn_on_red(led_pin_no, parking_no)
        logger.info(justify_logs(f"Car entered parking lot {parking_no}.", 44))
        body |= {"occupied": True}
        requests.put(url, json=body, headers=headers)
        logger.info(
            justify_logs(f"Sent request that parking lot {parking_no} is occupied.", 44)
        )
        return [True, True]
    elif distance >= 5 and sensor_state == [False, True]:
        led_control.turn_on_green(led_pin_no, parking_no)
        logger.info(f"Car left parking lot {parking_no}.")
        body |= {"occupied": False}
        requests.put(url, json=body, headers=headers)
        logger.info(
            justify_logs(f"Sent request that parking lot {parking_no} is emptied.", 44)
        )
        return [False, False]
    else:
        return [True if distance < 5 else False] + [sensor_state[0]]

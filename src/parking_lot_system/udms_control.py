import time
import os
import requests
import led_control
import RPi.GPIO as GPIO
import parking_lot_system.main_pi1 as main_pi1

logger = main_pi1.get_logger("udms_control")


def setup_udms(pin_list: list[int], sensor_no: int) -> None:
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
    logger.info(f"Setup of ultrasonic sensor {sensor_no} completed.")


def calculate_distance(pin_list: list[int], time_delta: int) -> float:
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
    led_pin_no: int,
    parking_no: int,
    garage_id: int,
) -> list[bool]:
    """
    Makes request about the state of the parking lot to the Backend.
    """
    url = "https://po3backend.ddns.net/api/rpi-parking-lot"
    headers = {"PO3-ORIGIN": "rpi", "PO3-RPI-KEY": os.environ["RPI_KEY"]}
    body = {"garageId": garage_id, "parkingLotNo": parking_no}
    if distance < 5 and sensor_state == [True, False]:
        logger.info(f"Car entered parking lot {parking_no}.")
        body |= {"occupied": True}
        requests.put(url, json=body, headers=headers)
        logger.info(f"Sent request that parking lot {parking_no} is occupied.")
        led_control.turn_on_red(led_pin_no, parking_no)
        return [True, True]
    elif distance >= 5 and sensor_state == [False, True]:
        logger.info(f"Car left parking lot {parking_no}.")
        body |= {"occupied": False}
        requests.put(url, json=body, headers=headers)
        logger.info(f"Sent request that parking lot {parking_no} is emptied.")
        led_control.turn_on_green(led_pin_no, parking_no)
        return [False, False]
    else:
        return [True if distance < 5 else False] + [sensor_state[0]]

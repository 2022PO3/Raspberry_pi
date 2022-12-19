from dotenv import load_dotenv


import RPi.GPIO as GPIO
import time
import reservation

from logger import get_logger, justify_logs

logger = get_logger("parking_lot_system")

PULSE_FREQUENCY = 50

GARAGE_ID = 11

load_dotenv()


def _setup_board() -> None:
    # Use pin numbers.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    logger.info(justify_logs("Setup of board completed.", 44))


def run_parking_lot_system(
    udms_pins: dict[int, tuple[int, int]],
    parking_led_pins: dict[int, tuple[int, int]],
    *,
    pi_no: int,
) -> None:
    import udms_control
    import led_control

    rng = range(1, 4) if pi_no == 1 else range(4, 7)

    # The states are an array of length 2. This prevents false positives. Only when the sensor
    # detects a car (or no car) for two consecutive times, the car will be detected. The first
    # element indicates most recent measurement.
    state_dict = {i: [False] * 2 for i in rng}

    _setup_board()
    for i in rng:
        udms_control.setup_udms(udms_pins[i], i)
        led_control.setup_led(parking_led_pins[i], i)
    logger.info(justify_logs("Setup of parking lot system completed.", 44))
    try:
        while True:
            reservation_dict = reservation.get_garage_reservations(GARAGE_ID)
            try:
                for i in rng:
                    distance = udms_control.calculate_distance(udms_pins[i], 1)
                    state_dict[i] = udms_control.update_parking_lot(
                        state_dict[i],
                        distance,
                        parking_led_pins[i],
                        i,
                        GARAGE_ID,
                        reservation_dict[i],
                    )
                    time.sleep(0.3)
            except Exception as e:
                logger.error(f"Some error occurred: {e}.")
    except KeyboardInterrupt:
        GPIO.cleanup()

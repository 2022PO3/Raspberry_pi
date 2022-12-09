"""
This code is for the parking lot system of the second Raspberry Pi.
"""


#####################
# Defining the pins #
#####################
# LED pins in the format `parking_lot_no: pin_no`. The pins are in the order [RED, GREEN].
PARKING_LED_PINS = {
    4: (23, 29),
    5: (31, 33),
    6: (35, 37),
}

# Pins for the ultrasonic sensors (the number refers to the parking lot number). The pins are
# in the order [TRIG, ECHO].
UDMS_PINS = {
    4: (11, 3),
    5: (13, 5),
    6: (15, 7),
}


if __name__ == "__main__":
    from main import run_parking_lot_system

    run_parking_lot_system(UDMS_PINS, PARKING_LED_PINS, pi_no=2)

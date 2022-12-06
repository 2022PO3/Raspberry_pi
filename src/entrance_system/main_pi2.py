"""
This code is for the entrance system of the second Raspberry Pi, which controls the exit of the garage.
"""

#####################
# Defining the pins #
#####################
ECHO_PIN = 18
TRIG_PIN = 16
SERVO_PIN = 12

if __name__ == "__main__":
    from entrance_system import run_entrance_system

    run_entrance_system(TRIG_PIN, ECHO_PIN, SERVO_PIN, system="exit")
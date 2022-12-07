# Raspberry_pi

This repository contains all the code which has to run on the Raspberry Pi, mainly written in Python.

To run the code on the Raspberry Pi, execute the following command:

```bash
bash start_pi.sh i
```

where `i` is the number of the Raspberry Pi which has to run. This will start the necessary Python scripts. The entrance system and the parking
lot system will start on both Pi's. Both Pi's power en run one camera and 3 ultrasonic distance measuring sensors. The first Pi will also power and control the 7-segment display

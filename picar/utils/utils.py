#!/usr/bin/env/python3
import time
from picar.motor import Pin


def reset_mcu():
    mcu_reset = Pin("MCURST")
    mcu_reset.off()
    time.sleep(0.001)
    mcu_reset.on()
    time.sleep(0.01)

#!/usr/bin/env/python3
"""
k_turn.py
Luke Strohbehn
"""
import picarx_improved as pcx
import logging
# import picarx.picarx_improved
import time
import atexit

RANGE = 1
ANGLE = 30
SPEED = 45

def parallel_park(px: pcx.Picarx, ANGLE=ANGLE, street_side:str ="right"):
    if street_side == "left":
        ANGLE = -ANGLE
    px.set_dir_servo_angle(0)

    for angle in range(ANGLE):
        logging.debug(f"ANGLE: {angle}")
        px.set_dir_servo_angle(angle)
        for j in range(RANGE):
            px.backward(SPEED)
            time.sleep(0.001)

    time.sleep(1)
    for angle in range(0, -ANGLE, -1):
        logging.debug(f"ANGLE: {angle}")
        px.set_dir_servo_angle(angle)
        for j in range(RANGE*20):
            px.forward(SPEED)
            time.sleep(0.001)


def main():
    px = pcx.Picarx()
    parallel_park(px)

    return px
    


if __name__ == "__main__":
    px = main()
    atexit.register(px.stop)
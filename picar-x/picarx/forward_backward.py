#!/usr/bin/env/python3
"""
forward_backward.py
Luke Strohbehn
"""
import picarx_improved as pcx


# import picarx.picarx_improved
import time
import atexit

SPEED = 100
ANGLE = 0

RANGE = 100


def main():
    px = pcx.Picarx()

    for i in range(RANGE):
        px.set_dir_servo_angle(-ANGLE)
        px.print_grayscale_data()
        px.forward(SPEED)
        time.sleep(0.001)
    return px


if __name__ == "__main__":

    px = main()

#!/usr/bin/env/python3
"""
circle.py
Luke Strohbehn
"""
from ..picarx_improved import Picarx
import time

SPEED = 20
ANGLE = 30


def main():
    px = Picarx()

    px.set_dir_servo_angle(self, ANGLE)
    px.set

    while True:
        px.get_dir_current_angle()
        px.forward(SPEED)
        time.sleep(0.001)


if __name__ == "__main__":
    main()
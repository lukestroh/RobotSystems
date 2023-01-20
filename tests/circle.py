#!/usr/bin/env/python3
"""
circle.py
Luke Strohbehn
"""
import picarx.picarx_improved as pcx


# import picarx.picarx_improved
import time

SPEED = 20
ANGLE = 30


def main():
    px = pcx.Picarx()

    px.set_dir_servo_angle(ANGLE)

    while True:
    
        px.forward(SPEED)
        time.sleep(0.001)


if __name__ == "__main__":
    main()
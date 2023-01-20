#!/usr/bin/env/python3
"""
circle.py
Luke Strohbehn
"""
import picarx.picarx_improved as pcx


# import picarx.picarx_improved
import time
import atexit

SPEED = 100
ANGLE = 30


def main():
    px = pcx.Picarx()

    px.set_dir_servo_angle(ANGLE)

    for i in range(1000):
        try:
            px.forward(SPEED)
            time.sleep(0.001)
        except KeyboardInterrupt:
            break
    for i in range(1000):
        px.set_dir_servo_angle(-ANGLE)
        try:
            px.forward(SPEED)
            time.sleep(0.001)
        except KeyboardInterrupt:
            break
    return px
    


if __name__ == "__main__":
    px = main()
    atexit.register(px.stop)
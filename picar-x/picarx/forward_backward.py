#!/usr/bin/env/python3
"""
circle.py
Luke Strohbehn
"""
import picarx_improved as pcx


# import picarx.picarx_improved
import time
import atexit

SPEED = .5
ANGLE = 20

RANGE = 1000


def main():
    px = pcx.Picarx()

    
    # px.set_dir_servo_angle(0)
    # for i in range(1000):
    #     px.forward(SPEED)
    # px.forward(0)
    # time.sleep(1)
    # for i in range(1000):
    #     px.backward(SPEED)

    for i in range(RANGE):
        px.set_dir_servo_angle(ANGLE)
        try:
            px.forward(SPEED)
            time.sleep(0.001)
        except KeyboardInterrupt:
            break
    
    # px.set_dir_servo_angle(0)
    # for angle in range(30):
    #     px.set_dir_servo_angle(angle)
    #     px.forward(SPEED)
    #     time.sleep(1)
    # return px

    # px.set_dir_servo_angle(-20)
    # for i in range(10000):
    #     px.forward(SPEED)
    #     # time.sleep(7)
    # px.forward(0)
    return px
    


if __name__ == "__main__":

    px = main()
    atexit.register(px.stop)
#!/usr/bin/env/python3
"""
parallel_park.py
Luke Strohbehn
"""
import picarx_improved as pcx


# import picarx.picarx_improved
import time
import atexit

RANGE = 5
ANGLE = 30
SPEED = 45

def parallel_park(px: pcx.Picarx, ANGLE=ANGLE, street_side:str ="right"):
    if street_side == "left":
        ANGLE = -ANGLE
    px.set_dir_servo_angle(ANGLE)

    for i in range(RANGE*20):
        px.backward(SPEED)
        time.sleep(0.001)

    # for angle in range(ANGLE):
    #     print(angle)
    #     px.set_dir_servo_angle(angle)
    #     for j in range(RANGE):
    #         px.backward(SPEED)
    #         time.sleep(0.001)


    for angle in range(ANGLE, 0, -1):
        print(angle)
        px.set_dir_servo_angle(angle)
        for j in range(int(RANGE*1.5)):
            px.backward(SPEED)
            time.sleep(0.001)

    px.set_dir_servo_angle(-ANGLE)

    for i in range(RANGE*50):
        px.backward(SPEED)
        time.sleep(0.001)

    px.forward(0)
    px.set_dir_servo_angle(0)
    time.sleep(1)
    for i in range(RANGE*30):
        px.forward(SPEED)
        time.sleep(0.001)

    # time.sleep(.2)

    # px.backward(SPEED)
    # time.sleep(1)

    # for angle in range(0, -ANGLE, -1):
    #     print(angle)
    #     px.set_dir_servo_angle(angle)
    #     for j in range(RANGE):
    #         px.backward(SPEED)
    #         time.sleep(0.001)
    px.forward(0)


def main():
    px = pcx.Picarx()
    parallel_park(px)

    return px
    


if __name__ == "__main__":
    px = main()
    atexit.register(px.stop)
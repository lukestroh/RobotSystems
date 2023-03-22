#!/usr/bin/env/python3
"""
move_forward.py
"""
from picar import picarx
import time


def main():
    try:
        px=picarx.Picarx()
        px.forward(40)
        time.sleep(60)
        px.stop()
        return 1
    except Exception as e:
        print(e)
        return 0



if __name__ == "__main__":
    main()
#!/usr/bin/env/python3
"""
circle.py
Luke Strohbehn
"""
import picarx_improved as pcx


# import picarx.picarx_improved
import time
import atexit

SPEED = 50
ANGLE = 20

RANGE = 1000


def main():
    px = pcx.Picarx()
    
    
    return px
    


if __name__ == "__main__":
    px = main()
    atexit.register(px.stop)
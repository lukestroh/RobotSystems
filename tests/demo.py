#!/usr/bin/env/python3
"""
main.py:
    Main program for running with user input
Luke Strohbehn
"""

import picar.picarx as pcx

from picar.user import user_input



def main():
    px = pcx.Picarx()

    _user_input = user_input(px)

    px.scheduler.run(_user_input)





    return




if __name__ == "__main__":
    main()
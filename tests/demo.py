#!/usr/bin/env python3
"""
main.py:
    Main program for running with user input
Luke Strohbehn
"""

import picar.picarx as pcx

from picar.user import user_input
import sys



def main():
    px = pcx.Picarx()

    
    _continue = True
    # while _continue:
    _user_input = user_input(px)
    if _user_input == "q":
        print("Thanks for testing out PiCarX! System shutting down.")
        px.cleanup()
        sys.exit()
    else:
        px.scheduler._run(_user_input)

    return

if __name__ == "__main__":
    main()
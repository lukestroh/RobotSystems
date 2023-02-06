#!/usr/bin/env/python3
"""
main.py:
    Main program for running with user input
Luke Strohbehn
"""
import picar
import picar.picarx as pcx



def main():
    px = pcx.Picarx()

    user_input = picar.user_input(px)

    px.utils.scheduler.run(user_input)





    return




if __name__ == "__main__":
    main()
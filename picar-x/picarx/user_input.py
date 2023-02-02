#!/usr/bin/env/python3
"""
user_input.py
Luke Strohbehn
"""
import picarx_improved as pcx




COMMAND_DICT: dict = {
    "1": "parallel_park",
    "2": "k_turn",
    "3": "follow line"
}


def main():

    px = pcx.Picarx()
    print(px.maneuver)

    print("What command do you want to run?")
    for key, value in COMMAND_DICT.items():
        print(key, value)

    comm = int(input("Please enter the number of the command and hit enter:\n").strip())

    if comm == 1:
        px.maneuver.parallel_park()
    elif comm == 2:
        px.maneuver.k_turn()
    elif comm == 3:
        px.maneuver.follow_line()

    return


if __name__ == "__main__":
    main()

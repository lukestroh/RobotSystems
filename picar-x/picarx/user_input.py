#!/usr/bin/env/python3
"""
user_input.py
Luke Strohbehn
"""
import k_turn, parallel_park


COMMAND_DICT: dict = {"1": "parallel park", "2": "K-turn"}


def main():
    print("What command do you want to run?")
    for key, value in COMMAND_DICT.items():
        print(key, value)

    comm = int(input("Please enter the number of the command and hit enter:\n").strip())

    
    if comm == 1:
        parallel_park.main()
    elif comm == 2:
       k_turn.main()

    return


if __name__ == "__main__":
    main()

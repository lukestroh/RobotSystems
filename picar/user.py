#!/usr/bin/env/python3
"""
user_input.py
Luke Strohbehn
"""


def user_input(px):
    print("What command do you want to run?")
    for key, value in px.COMMAND_DICT.items():
        print(key, value)

    return int(input("Please enter the number of the command and hit enter:\n").strip())

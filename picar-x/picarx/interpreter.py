#!/usr/bin/env/python3

"""
interpret.py
Luke Strohbehn
"""

import picarx_improved as pcx

class Interpreter():

    def __init__(self, light_idx, dark_idx, polarity="light") -> None:
        self.light_idx = light_idx
        self.dark_idx = dark_idx
        self.polarity = polarity

    def follow_path(self, greyscale_data) -> int:
        
        if self.polarity == "light":
            if greyscale_data[0] < self.light_idx and greyscale_data[1] < self.light_idx and greyscale_data[2] < self.light_idx:
                return -1

            if 

        else:
            pass

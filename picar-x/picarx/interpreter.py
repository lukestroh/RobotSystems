#!/usr/bin/env/python3

"""
interpret.py
Luke Strohbehn
"""

import picarx_improved as pcx
# import numpy as np

class Interpreter():

    def __init__(self, light_idx, dark_idx, polarity="light") -> None:
        self.light_idx = light_idx
        self.dark_idx = dark_idx
        self.polarity = polarity

    def follow_path(self, greyscale_data) -> int:

        if self.polarity == "light":
            # if greyscale_data[0] < self.light_idx and greyscale_data[1] < self.light_idx and greyscale_data[2] < self.light_idx:
            #     return -1

            # if 

            G_x = [1, 2, 1] * ([2,0,-2] * greyscale_data)
            return G_x
        else:
            pass

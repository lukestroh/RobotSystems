#!/usr/bin/env/python3

"""
interpret.py
Luke Strohbehn
"""

# import picarx_improved as pcx
from numpy import mean
import scipy as sp
from typing import List
from collections import deque

class GreyscaleInterpreter():

    def __init__(self, light_idx:int, dark_idx:int, polarity:str="dark") -> None:
        self.light_idx = light_idx
        self.dark_idx = dark_idx
        self.polarity = polarity


        self.deriv_thresh = 100 # adjust for sensitivity

        self.deque_len = 20
        self.left_deq = deque([], maxlen=self.deque_len)
        self.mid_deq = deque([], maxlen=self.deque_len)
        self.right_deq = deque([], maxlen=self.deque_len)

    def set_initial_gs_vals(self, greyscale_data:List[int, int, int]):
        self.left_prev = greyscale_data[0]
        self.mid_prev = greyscale_data[1]
        self.right_prev = greyscale_data[2]

    def get_steering_idx(self, _input: int, min1:float=0, max1:float=1500, min2:float=0, max2:float = 1.0) -> float:
        return (_input/(max1 - min1)*(max2 - min2))
        

    def follow_path_comm(self, greyscale_data: List[int, int, int]) -> float:
        self.left_curr = greyscale_data[0]
        self.mid_curr = greyscale_data[1]
        self.right_curr = greyscale_data[2]

        """ Get the average of the right and left to determine how much to turn? """

        left_avg = mean(self.left_deq)
        mid_avg = mean(self.mid_deq)
        right_avg = mean(self.right_deq)

        # some code here
        left_diff = left_avg - self.left_curr
        mid_diff = mid_avg - self.mid_curr
        right_diff = right_avg - self.right_curr

        # add to the deques before we return values
        self.left_deq.append(self.left_curr)
        self.mid_deq.append(self.mid_curr)
        self.right_deq.append(self.right_curr)

        # off track case
        if left_diff > self.deriv_thresh and right_diff > self.deriv_thresh and mid_diff > self.deriv_thresh:
            return None
        #
        if abs(left_diff) > self.deriv_thresh:
            return -1.0 * self.get_steering_idx(mean([self.left_curr, self.right_curr]))
        elif abs(right_diff) > self.deriv_thresh:
            return self.get_steering_idx(mean([self.left_curr, self.right_curr]))
        else:
            return 0

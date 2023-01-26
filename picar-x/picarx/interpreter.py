#!/usr/bin/env/python3

"""
interpret.py
Luke Strohbehn
"""

# import picarx_improved as pcx
import numpy as np
import scipy as sp
from typing import List
from collections import deque

class Interpreter():

    def __init__(self, light_idx:int, dark_idx:int, polarity:str="light") -> None:
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

    def get_steering_idx(self, _input: int, min1:float=0, max1:float=1500, min2:float =-1.0, max2:float = 1.0) -> float:
        return (_input/(max1 - min1)*(max2 - min2))
        

    def follow_path_comm(self, greyscale_data: List[int, int, int]) -> float:
        # self.left_curr = greyscale_data[0]
        # self.mid_curr = greyscale_data[1]
        # self.right_curr = greyscale_data[2]

        # self.left_grad = self.left_curr - self.left_prev
        # self.mid_grad = self.mid_curr - self.mid_prev
        # self.right_grad = self.right_curr - self.right_prev

        left_avg = mean(self.left_deq)
        mid_avg = mean(self.mid_deq)
        right_avg = mean(self.right_deq)


        self.left_deq.append(greyscale_data[0])
        self.mid_deq.append(greyscale_data[1])
        self.right_deq.append(greyscale_data[2])




        # # some code here
        # if self.left_grad > self.deriv_thresh and self.right_grad > self.deriv_thresh and self.mid_grad > self.deriv_thresh:
        #     return None
        
        # # left side correction
        # elif self.left_grad > self.deriv_thresh and self.mid_grad > self.deriv_thresh:

        #     pass

        # # right side correction
        # elif self.right_grad > self.deriv_thresh and self.mid_grad > self.deri


        # #

        # self.left_prev = self.left_curr
        # self.mid_prev = self.mid_curr
        # self.right_prev = self.right_curr




        # """
        # Parameters
        # ----------
        #     greyscale_data (List[int, int, int])

        # Returns
        # -------
        #     direction (int):
        #         -1: stop (path has been lost)
        #         0: continue along path (either forward or backward)
        #         1: car is to the left of the line (from the driver's perspective)
        #         2: car is to the right of the line (from the driver's perspective)
        # """
        # self.left_diff = greyscale_data[0] - greyscale_data[1]
        # self.right_diff = greyscale_data[2] - greyscale_data[1]
        
        # if self.polarity == "light":
        #     if greyscale_data[0] < self.light_idx and greyscale_data[1] < self.light_idx and greyscale_data[2] < self.light_idx:
        #         return None
        #     if right_diff > left_diff:
        #         return self.get_steering_idx()
        #     elif left_diff > right_diff:
        #         return 2
        #     else:
        #         return 0

        # else:
        #     pass

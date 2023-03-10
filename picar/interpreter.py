#!/usr/bin/env/python3

"""
interpret.py
Luke Strohbehn
"""

# import picarx_improved as pcx
from numpy import mean

# import scipy as sp
from typing import List
from collections import deque
import logging
import time

from picar.utils.bus import InterpreterBus


logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)


class GrayscaleInterpreter:
    def __init__(self, px, light_idx: int, dark_idx: int, polarity: str = "dark") -> None:
        self.light_idx = light_idx
        self.dark_idx = dark_idx
        self.polarity = polarity

        self.deriv_thresh = 300  # adjust for sensitivity
        self.MAX_ADC = 1500
        self.max_steer_angle = 30

        self.deque_len = 35
        self.left_deq = deque([], maxlen=self.deque_len)
        self.mid_deq = deque([], maxlen=self.deque_len)
        self.right_deq = deque([], maxlen=self.deque_len)

        # Bus
        self.grayscale_bus = px.grayscale_bus
        self.interpreter_bus = px.interpreter_bus = InterpreterBus()

    def set_initial_gs_vals(self, greyscale_data: List[int]) -> None:
        self.left_deq.append(greyscale_data[0])
        self.mid_deq.append(greyscale_data[1])
        self.right_deq.append(greyscale_data[2])

    def get_steering_scale(self, greyscale_data: List[int]) -> float:
        self.left_curr = greyscale_data[0]
        self.mid_curr = greyscale_data[1]
        self.right_curr = greyscale_data[2]

        """ Get the average of the right and left to determine how much to turn? """

        left_avg = mean(self.left_deq)
        mid_avg = mean(self.mid_deq)
        right_avg = mean(self.right_deq)

        # sensor average differences
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

        # sensor side differences
        left_mid_der = self.left_curr - mid_avg
        right_mid_der = self.right_curr - mid_avg

        total_diff = left_mid_der - right_mid_der
        scaled_diff = total_diff / self.MAX_ADC
        logging.debug(f"{scaled_diff}")

        return scaled_diff

    def map_steer_idx_to_angle(self, steer_scale):
        if steer_scale is None:
            pass
        else:
            return steer_scale * self.max_steer_angle

    def follow_line(self, greyscale_data: List[int]):
        steer_scale = self.get_steering_scale(greyscale_data)
        if steer_scale is None:
            return None
        else:
            steer_angle = self.map_steer_idx_to_angle(steer_scale)
            return steer_angle

    def read_sensor_bus(self):
        return self.grayscale_bus.read()

    def write_interpreter_bus(self, message):
        return self.interpreter_bus.write(message)

    def run(self, time_delay):
        while True:
            self.write_interpreter_bus(self.read_sensor_bus())
            time.sleep(time_delay)


def main():
    return


if __name__ == "__main__":
    main()

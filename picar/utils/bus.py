#!/usr/bin/env/python3
"""
bus.py
Luke Strohbehn
"""

from picar.utils.basicbus import BasicBus
from typing import Any
import time


class ControllerBus(BasicBus):
    def __init__(self) -> None:
        super().__init__()

        pass


class GrayscaleBus(BasicBus):
    def __init__(self) -> None:
        super().__init__()
        return

    def run(self, time_limit):
        while self.message:

            time.sleep(time_limit)
        return


class CameraBus(BasicBus):
    def __init__(self) -> None:
        super().__init__()

        pass


class UltrasonicBus(BasicBus):
    def __init__(self) -> None:
        super().__init__()
        pass


class InterpreterBus(BasicBus):
    def __init__(self) -> None:
        super().__init__()

        # make a dictionary for each of the types of data, (and give them priority numbers?)

        pass

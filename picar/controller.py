#!/usr/bin/env/python3

from picar.utils.bus import InterpreterBus, UltrasonicBus

from picar.picarx import Picar

import time
from typing import Any


class Controller:
    def __init__(self, px: Picar) -> None:
        self.control_data = {}
        self.interpreter_bus = px.interpreter_bus
        self.ultrasonic_bus = px.ultrasonic_bus
        return

    def read_interpreter_bus(self):
        return self.interpreter_bus.read()

    def read_ultrasonic_bus(self) -> Any:
        return self.ultrasonic_bus.read()

    # need some publisher functions here

    def run(self, time_delay: float) -> None:

        while self.px.run:
            # get interpreter data
            self.control_data["interpreter_data"] = self.read_interpreter_bus(self)

            # get ultrasonic data, maybe make loop more frequent?
            self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus(self)

            # do something, if completed, self.run = False

            

            time.sleep(time_delay)

    def read_controller_bus():
        return

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
        self.px = px
        return

    def read_interpreter_bus(self):
        return self.interpreter_bus.read()

    def read_ultrasonic_bus(self) -> Any:
        return self.ultrasonic_bus.read()

    def get_maneuver(self, user_input: str) -> None:
        user_command = self.px.COMMAND_DICT[user_input]
        if user_command == "parallel_park":
            self.px.maneuver.parallel_park()
        elif user_command == "k_turn":
            self.px.maneuver.k_turn()
        elif user_command == "follow_line":
            self.px.maneuver.follow_line()
        return

    # need some publisher functions here

    def _run(self, time_delay: float, user_input) -> None:
        while self.px.run:
            # get interpreter data
            self.control_data["interpreter_data"] = self.read_interpreter_bus(self)

            # get ultrasonic data, maybe make loop more frequent?
            self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus(self)

            # do something, if completed, self.px.run = False
            self.get_maneuver(user_input)

            time.sleep(time_delay)

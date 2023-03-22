#!/usr/bin/env python3

from picar.utils.bus import InterpreterBus, UltrasonicBus

import time
from typing import Any


class Controller:
    def __init__(self, px) -> None:
        self.control_data = {}
        self.interpreter_bus = px.interpreter_bus
        self.ultrasonic_bus = px.ultrasonic_bus
        self.px = px
        self.car_speed = 40

        self.actions: dict = {

        }
        self.name = "controller"
        return

    def read_interpreter_bus(self):
        return self.interpreter_bus.read(tag=self.name)

    def read_ultrasonic_bus(self) -> Any:
        return self.ultrasonic_bus.read(tag=self.name)

    def get_maneuver(self, user_input: str) -> None:
        user_command = self.px.COMMAND_DICT[user_input]
        if user_command == "parallel_park":
            self.px.maneuver.parallel_park()
        elif user_command == "k_turn":
            self.px.maneuver.k_turn()
        elif user_command == "follow_line":
            self.px.maneuver.follow_line()
        return


    def _run(self, time_delay: float, user_input) -> None: # maybe could operate this as an *args **kwargs situation



        while self.px.run:
            # get ultrasonic data, maybe make loop more frequent? Or maybe the ultrasonic should have its own controller?
            self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus(self)
            if self.control_data["ultrasonic_data"] < 10:
                self.px.stop()


            # get interpreter data
            self.control_data["interpreter_data"] = self.read_interpreter_bus(self)

            

            ##### Right now, the steering angle is being determined in Interpreter.py, which seems like the wrong place. 
            # Since the angle is calculated in the interpreter though, i'll need a system-wide variable that holds the task that we're doing?
            # Yes I think I like that.

            # # do something, if completed, self.px.run = False
            # self.get_maneuver(user_input)

            self.px.set_dir_servo_angle(self.control_data["interpreter_data"]["steering_angle"])
            self.px.foward(self.car_speed)
            time.sleep(time_delay)




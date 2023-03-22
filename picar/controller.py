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
        self.car_speed = 20

        self.actions: dict = {

        }
        self.name = "controller"
        return

    def read_interpreter_bus(self):
        return self.interpreter_bus.read(tag=self.name)

    def read_ultrasonic_bus(self) -> Any:
        return self.ultrasonic_bus.read(tag=self.name)

    # def get_maneuver(self, user_input: str) -> None:
    #     user_command = self.px.COMMAND_DICT[user_input]
    #     if user_command == "parallel_park":
    #         self.px.maneuver.parallel_park()
    #     elif user_command == "k_turn":
    #         self.px.maneuver.k_turn()
    #     elif user_command == "follow_line":
    #         self.px.maneuver.follow_line()
    #     return

    def run_once(self):
        # get interpreter data
        self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus()
        self.control_data["interpreter_data"] = self.read_interpreter_bus()
        # print(self.control_data)
        return self.control_data

        

        ##### Right now, the steering angle is being determined in Interpreter.py, which seems like the wrong place. 
        # Since the angle is calculated in the interpreter though, i'll need a system-wide variable that holds the task that we're doing?
        # Yes I think I like that.

        # # do something, if completed, self.px.run = False
        # self.get_maneuver(user_input)

        

        # update ultrasonic data before the next loop
        



    def _run(self, time_delay: float, user_input=None) -> None: # maybe could operate this as an *args **kwargs situation

        self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus()

        while self.px.run:

            while self.control_data["ultrasonic_data"] > 10:
                # get ultrasonic data, maybe make loop more frequent? Or maybe the ultrasonic should have its own controller?
                


                # get interpreter data
                self.control_data["interpreter_data"] = self.read_interpreter_bus()

                #### That means these are going to throw errors... ? because the functions aren't declared yet?
                self.px.set_dir_servo_angle(self.control_data["interpreter_data"]["steering_angle"])
                self.px.foward(self.car_speed)

                # thread loop delay
                time.sleep(time_delay)

                # update ultrasonic data before the next loop
                self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus()


            while self.control_data["ultrasonic_data"] <= 10:
                print(self.read_ultrasonic_bus())
                # get interpreter data
                self.control_data["interpreter_data"] = self.read_interpreter_bus()

                time.sleep(time_delay) # just sleep a bit longer? Make this larger once we make sensor input quicker
                self.control_data["ultrasonic_data"] = self.read_ultrasonic_bus()



def main():
    from picar.picarx import Picarx

    px = Picarx()
    px.run = True

    while True:
        px.ultrasonic_sensor.write_ultrasonic_bus(px.ultrasonic_sensor.read())

# input()
            
        
        px.grayscale_sensor.write_grayscale_bus(px.grayscale_sensor.get_grayscale_data()) # should change this function name to read()
        px.interpreter.run_once()
    
        control_data = px.controller.run_once()
        px.set_dir_servo_angle(control_data["interpreter_data"]["steering_angle"])
        if control_data["ultrasonic_data"] > 10:
            px.forward(40)
        else:
            px.stop()


    return


if __name__ == "__main__":
    main()
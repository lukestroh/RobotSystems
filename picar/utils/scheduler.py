#!/usr/bin/env python3
"""
scheduler.py
Luke Strohbehn
"""
import concurrent.futures as cf
import logging


logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)


class Scheduler:
    def __init__(self, px) -> None:
        self.px = px
        self.maneuver = px.maneuver
        self.grayscale_sensor = px.grayscale_sensor
        self.ultrasonic_sensor = px.ultrasonic_sensor
        self.interpreter = px.interpreter
        self.controller = px.controller
        
        return

    def _run(self, user_input):
        # delays
        self.px.run = True

        grayscale_delay = 0.5
        interpreter_delay = 0.5
        controller_delay = 0.5
        ultrasonic_delay = 0.5

        try:
            with cf.ThreadPoolExecutor(max_workers=3) as executor:
                # ultrasonic
                ultrasonic = executor.submit(self.ultrasonic_sensor._run, ultrasonic_delay)

                # grayscale
                grayscale = executor.submit(self.grayscale_sensor._run, grayscale_delay)
                # logging.debug(f"grayscale: {grayscale}")

                # interpreter
                interpreter = executor.submit(self.interpreter._run, interpreter_delay)
                # logging.debug(f"interpreter: {interpreter}")

                # controller
                controller = executor.submit(self.controller._run, controller_delay, user_input)
                
                # wait for the 
                processes = [ultrasonic, grayscale, interpreter, controller]
                print(processes)

                # cf.wait waits for the Future objects have completed. 
                # Options include "FIRST_EXCEPTION", "FIRST_COMPLETED", and "ALL_COMPLETED"
                cf.wait(processes, return_when="FIRST_EXCEPTION")

                """
                [<Future at 0xb54d9fb0 state=finished raised AttributeError>, <Future at 0xb54eb1f0 state=running>, <Future at 0xb54ebd70 state=running>, <Future at 0xb54ebef0 state=pending>]
                """

            ultrasonic.result()
            grayscale.result()
            interpreter.result()
            controller.result()

        except Exception as e:
            self.px.run = False
            print(e)

        return

    def run_until_complete(self, user_input):
        self.run = True
        while self.run:
            self._run(user_input)
        return

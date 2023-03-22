#!/usr/bin/env/python3
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
        self.interpreter = px.interpreter
        self.controller = px.controller
        return

    def _run(self, user_input):
        # delays
        self.px.run = True

        grayscale_delay = 0.5
        interpreter_delay = 0.5
        controller_delay = 0.5
        us_controller_delay = 0.5

        try:
            with cf.ThreadPoolExecutor(max_workers=3) as executor:
                # grayscale
                grayscale = executor.submit(self.grayscale_sensor._run, grayscale_delay)
                # logging.debug(f"grayscale: {grayscale}")

                # interpreter
                interpreter = executor.submit(self.interpreter._run, interpreter_delay)
                # logging.debug(f"interpreter: {interpreter}")

                # controller
                controller = executor.submit(self.controller._run, controller_delay, user_input)
                
                # wait for the 
                processes = [grayscale, interpreter, controller]
                cf.wait(processes, return_when="FIRST_COMPLETED")
            # interpreter.result()

        except Exception as e:
            self.px.run = False
            print(e)

        return

    def run_until_complete(self, user_input):
        self.run = True
        while self.run:
            self._run(user_input)
        return

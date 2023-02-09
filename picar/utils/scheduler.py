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
        self.run = px.run
        return

    def run(self, user_input) -> bool:
        # delays
        self.px.run = True

        grayscale_delay = 0.5
        interpreter_delay = 0.5

        try:

            # executor
            executor = cf.ThreadPoolExecutor(max_workers=3)
            grayscale = executor.submit(self.px.grayscale_sensor.run, grayscale_delay)
            logging.debug(f"grayscale: {grayscale}")
            
            interpreter = executor.submit(self.px.interpreter.run, interpreter_delay)
            logging.debug(f"interpreter: {interpreter}")


            # print(grayscale)
            # print(interpreter)
        except Exception as e:
            self.run = False
            print(e)

        return

    def run_until_complete(self, user_input):
        while True:
            self.run(user_input)
        return

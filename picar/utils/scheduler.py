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
        return

    def run(self, user_input):
        # delays
        grayscale_delay = 0.5
        interpreter_delay = 0.5

        # executor
        with cf.ThreadPoolExecutor(max_workers=3) as executor:
            eSensor = executor.submit(self.px.grayscale_sensor.run, grayscale_delay)
            logging.debug(f"eSensor: {eSensor}")
            
            interpreter = executor.submit(self.px.interpreter.run, interpreter_delay)
            logging.debug(f"interpreter: {interpreter}")

            for future in cf.as_completed(eSensor):
                data1 = eSensor[future]
                logging.debug(f"Data 1: {data1}")
                try:
                    data2 = future.result()
                    logging.debug(f"Data 2: {data2}")
                except Exception as e:
                    print(e)


            # eInterpreter = executor.submit(interpreter_function, sensor_values_bus, interpreter_delay)

        eSensor.result()  # displays erros
        # eInterpreter.result()

        print(eSensor)
        # print(eInterpreter)

        return

    def run_until_complete(self, user_input):
        while True:
            self.run(user_input)
        return

#!/usr/bin/env/python3

import concurrent.futures as cf


class Scheduler():
    def __init__(self) -> None:
        pass

    def run(self):
        with cf.ThreadPoolExecutor(max_workers=3) as executor:
            eSensor = executor.submit(sensor_function, sensor_values_bus, sensor_delay)
            
            eInterpreter = executor.submit(interpreter_function, sensor_values_bus, interpreter_delay)

        eSensor.result() # displays erros

        return
#!/usr/bin/env/python3

import concurrent.futures as cf


class Scheduler():
    def __init__(self, px) -> None:
        self.px = px
        return

    def run(self, user_input):
        grayscale_delay = 0.5
        with cf.ThreadPoolExecutor(max_workers=3) as executor:
            eSensor = executor.submit(self.px.grayscale_sensor.run, self.px.grayscale_bus.run, grayscale_delay)
            
            # eInterpreter = executor.submit(interpreter_function, sensor_values_bus, interpreter_delay)

        eSensor.result() # displays erros
        # eInterpreter.result()

        print(eSensor)
        # print(eInterpreter)


        return
    
    def run_until_complete(self):
        while True:
            self.run()
        return
#!/usr/bin/env python3

from picar import picarx


def main():
    

    px = picarx.Picarx()
    px.run = True

    while True:
        px.ultrasonic_sensor.write_ultrasonic_bus(px.ultrasonic_sensor.read())

# input()
            
        
        px.grayscale_sensor.write_grayscale_bus(px.grayscale_sensor.get_grayscale_data()) # should change this function name to read()
        px.interpreter.run_once()
    
        control_data = px.controller.run_once()
        
        if control_data["ultrasonic_data"] > 10:
            px.set_dir_servo_angle(control_data["interpreter_data"]["steering_angle"])
            px.forward(20)

        else:
            px.stop()


    return


if __name__ == "__main__":
    main()
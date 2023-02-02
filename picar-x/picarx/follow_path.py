#!/usr/bin/env/python3
"""
follow_path.py
Luke Strohbehn
"""


import picarx_improved as pcx

SPEED = 40
MAX_STEER_ANGLE = 35


def map_steer_idx_to_angle(steer_val: float) -> float:
    return steer_val / (1) * 30


### steering function folloiwng cot(theta) so that servo doesn't jerk around?

def main():
    px = pcx.Picarx()
    px.gs_interpreter.set_initial_gs_vals(px.get_grayscale_data())


    try:
        while True:
            gs_data = px.get_grayscale_data()
            
            steer_angle = px.gs_interpreter.follow_line(gs_data)
            if steer_angle is None:
                px.stop()
            else: 
                px.set_dir_servo_angle(steer_angle)
                px.forward(SPEED)
    except KeyboardInterrupt:
        px.stop()


if __name__ == "__main__":
    main()

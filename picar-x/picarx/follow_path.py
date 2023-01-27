#!/usr/bin/env/python3
"""
follow_path.py
Luke Strohbehn
"""


import picarx_improved as pcx

SPEED = 40
MAX_STEER_ANGLE = 35


def map_steer_idx_to_angle(steer_val: float) -> float:
    return steer_val / (1) * 35


def main():
    px = pcx.Picarx()
    px.gs_interpreter.set_initial_gs_vals(px.get_grayscale_data())

    try:
        while True:
            gs_data = px.get_grayscale_data()
            steer_val = px.gs_interpreter.follow_path_comm(gs_data)
            if steer_val is None:
                px.stop()
            elif steer_val == 0:
                px.forward(SPEED)
            else:
                px.set_dir_servo_angle(map_steer_idx_to_angle(steer_val))
                px.forward(SPEED)
    except KeyboardInterrupt:
        px.stop()
        return


if __name__ == "__main__":
    main()

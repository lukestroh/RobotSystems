#!/usr/bin/env/python3
"""
maneuver.py
Luke Strohbehn
"""
import time
import logging


class Maneuver():
    def __init__(self, px) -> None:
        self.maneuver_angle = 30
        self.maneuver_speed = 40
        self.range = 1
        self.px = px
        pass

    
    def forward_backward(self, forward=True, angle=0):
        if forward:
            for i in range(self.range):
                self.px.set_dir_servo_angle(angle)
                self.px.forward(self.maneuver_speed)
                time.sleep(0.001)

            self.px.stop()

        else:
            for i in range(self.range):
                self.px.set_dir_servo_angle(angle)
                self.px.backward(self.maneuver_speed)
        return

    def k_turn(self, street_side: str = "right"):
        angle = self.maneuver_angle
        if street_side == "left":
            angle = -angle
        self.px.set_dir_servo_angle(0)

        for _a in range(0, -angle, -1):
            # logging.debug(f"ANGLE: {angle}")
            self.px.set_dir_servo_angle(_a)
            for j in range(self.range):
                self.px.forward(self.maneuver_speed)
                time.sleep(0.001)
        time.sleep(1)

        for _a in range(0, angle, 1):
            # logging.debug(f"ANGLE: {angle}")
            self.px.set_dir_servo_angle(_a)
            for j in range(self.range):
                self.px.backward(self.maneuver_speed)
                time.sleep(0.001)
        time.sleep(1)

        # Equation for perimeter of ellipse
        # p = 4*a*integral[0,pi/2] (sqrt(1-e^2*sin^2(theta))*dTheta)
        # where e is the eccentricity of the ellipse

        # while True:
        #     px.set_dir_servo_angle(-ANGLE)
        self.forward(0)
        return


    def parallel_park(self, street_side: str = "right"):
        if street_side == "right":
            angle = -self.maneuver_angle
            self.px.set_dir_servo_angle(angle)

            for i in range(self.range * 20):
                self.px.backward(self.maneuver_speed)
                time.sleep(0.001)

            for _a in range(angle, 0, -1):
                print(angle)
                self.px.set_dir_servo_angle(_a)
                for j in range(int(self.range * 1.5)):
                    self.px.backward(self.maneuver_speed)
                    time.sleep(0.001)

            self.px.set_dir_servo_angle(-angle)

            for i in range(self.range * 50):
                self.px.backward(self.maneuver_speed)
                time.sleep(0.001)

            self.px.forward(0)
            self.px.set_dir_servo_angle(0)
            time.sleep(1)
            for i in range(self.range * 30):
                self.px.forward(self.maneuver_speed)
                time.sleep(0.001)

            self.px.forward(0)
            return



    def follow_line(self):
        self.px.gs_interpreter.set_initial_gs_vals(self.px.get_grayscale_data())
        try:
            while True:
                gs_data = self.px.get_grayscale_data()
                
                steer_angle = self.px.gs_interpreter.follow_line(gs_data)
                if steer_angle is None:
                    self.px.stop()
                else: 
                    self.px.set_dir_servo_angle(steer_angle)
                    self.px.forward(self.maneuver_speed)
        except KeyboardInterrupt:
            self.px.stop()

        return




    
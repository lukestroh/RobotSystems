import logging
from logdecorator import log_on_start, log_on_end, log_on_error


import atexit

# try:
#     from robot_hat import *
#     from robot_hat.utils import reset_mcu

#     reset_mcu()
#     time.sleep(0.01)
# except (ImportError, ModuleNotFoundError):
#     print(
#         "This computer does not appear to be a PiCar-X system (robot_hat is not present). Shadowing hardware calls with substitute functions."
#     )
#     from sim_robot_hat import *

import os
import time
import numpy as np


# try:
#     # import picar
from picar.motor import Pin, PWM, Servo

from picar.sensor import I2C, GrayscaleSensor, UltrasonicSensor
from picar.interpreter import GrayscaleInterpreter
from picar.maneuver import Maneuver

from picar.utils.scheduler import Scheduler
from picar.utils.bus import GrayscaleBus, UltrasonicBus, InterpreterBus

from picar.utils.filedb import fileDB
from picar.utils.utils import reset_mcu

reset_mcu()
time.sleep(0.01)
# except (ImportError, ModuleNotFoundError):
#     print(
#         "This computer does not appear to be a PiCar-X system (robot_hat is not present). Shadowing hardware calls with substitute functions."
#     )
#     from picar.sim_robot_hat import *


logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)


# user and User home directory
User = os.popen("echo ${SUDO_USER:-$LOGNAME}").readline().strip()
UserHome = os.popen("getent passwd %s | cut -d: -f 6" % User).readline().strip()
# print(User)  # pi
# print(UserHome) # /home/pi
config_file = "%s/.config/picar-x/picar-x.conf" % UserHome


class Picarx(object):
    PERIOD = 4095
    PRESCALER = 10
    TIMEOUT = 0.02

    # servo_pins: direction_servo, camera_servo_1, camera_servo_2
    # motor_pins: left_swicth, right_swicth, left_pwm, right_pwm
    # grayscale_pins: 3 adc channels
    # ultrasonic_pins: tring, echo
    # config: path of config file
    @log_on_end(logging.DEBUG, "Initialized PicarX")
    def __init__(
        self,
        servo_pins: list = ["P0", "P1", "P2"],
        motor_pins: list = ["D4", "D5", "P12", "P13"],
        grayscale_pins: list = ["A0", "A1", "A2"],
        ultrasonic_pins: list = ["D2", "D3"],
        config: str = config_file,
    ):
        # user input dictionary
        self.COMMAND_DICT: dict = {"1": "parallel_park", "2": "k_turn", "3": "follow line"}
        self.ACTIVE_COMMAND: str
        # Car dimensions
        self.LENGTH_CHASSIS: float = 9.36625  # cm 3 + 11/16 in
        self.WIDTH_BACK_WHEELBASE: float = 11.43  # cm 4.5 in
        self.LENGTH_FRONT_WHEELBASE: float = 10.75
        self.FRONT_WHEEL_DI: float = 6.6
        self.BACK_WHEEL_DI: float = 6.58
        # config_flie
        self.config_flie = fileDB(config, 774, User)
        # servos init
        self.camera_servo_pin1 = Servo(PWM(servo_pins[0]))
        self.camera_servo_pin2 = Servo(PWM(servo_pins[1]))
        self.dir_servo_pin = Servo(PWM(servo_pins[2]))
        self.dir_cal_value = int(self.config_flie.get("picarx_dir_servo", default_value=0))
        self.cam_cal_value_1 = int(self.config_flie.get("picarx_cam_servo1", default_value=0))
        self.cam_cal_value_2 = int(self.config_flie.get("picarx_cam_servo2", default_value=0))
        self.dir_servo_pin.angle(self.dir_cal_value)
        self.camera_servo_pin1.angle(self.cam_cal_value_1)
        self.camera_servo_pin2.angle(self.cam_cal_value_2)
        # motors init
        self.left_rear_dir_pin = Pin(motor_pins[0])
        self.right_rear_dir_pin = Pin(motor_pins[1])
        self.left_rear_pwm_pin = PWM(motor_pins[2])
        self.right_rear_pwm_pin = PWM(motor_pins[3])
        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        self.cali_dir_value = self.config_flie.get("picarx_dir_motor", default_value="[1,1]")
        self.cali_dir_value = [int(i.strip()) for i in self.cali_dir_value.strip("[]").split(",")]
        self.cali_speed_value = [0, 0]
        self.dir_current_angle = 0
        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)


        # need to make it so that each sensor/interpreter/control generates it's own bus so that instantiation works.

        # Bus (bus instantiation is in each sensor/interpreter class)
        self.grayscale_bus: GrayscaleBus
        self.ultrasonic_bus: UltrasonicBus
        self.interpreter_bus: InterpreterBus


        # Sensor
        adc0, adc1, adc2 = grayscale_pins
        self.grayscale_sensor = GrayscaleSensor(self, adc0, adc1, adc2, reference=1000)
        # ultrasonic init
        # usage: distance = self.ultrasonic.read()
        tring, echo = ultrasonic_pins
        self.ultrasonic = UltrasonicSensor(Pin(tring), Pin(echo))
        
        # Interpreter
        self.gs_interpreter = GrayscaleInterpreter(self, light_idx=1000, dark_idx=500, polarity="light")

        # Scheduler
        self.scheduler = Scheduler(self)
        
        # Maneuver
        self.maneuver = Maneuver(self)

        # at exit
        atexit.register(self.cleanup)
        return

    def set_motor_speed(self, motor, speed):
        # global cali_speed_value,cali_dir_value
        motor -= 1
        if speed >= 0:
            direction = 1 * self.cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        # if speed != 0:
        # speed = int(speed / 2) + 50
        speed = speed - self.cali_speed_value[motor]
        # logging.debug(f"{motor+1}: {speed}")
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)

    def motor_speed_calibration(self, value):
        # global cali_speed_value,cali_dir_value
        self.cali_speed_value = value
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(self.cali_speed_value)
        else:
            self.cali_speed_value[0] = abs(self.cali_speed_value)
            self.cali_speed_value[1] = 0

    def motor_direction_calibration(self, motor, value):
        # 1: positive direction
        # -1:negative direction
        motor -= 1
        if value == 1:
            self.cali_dir_value[motor] = -1 * self.cali_dir_value[motor]
        self.config_flie.set("picarx_dir_motor", self.cali_dir_value)
        if value == 1:
            self.cali_dir_value[motor] = 1
        elif value == -1:
            self.cali_dir_value[motor] = -1
        self.config_flie.set("picarx_dir_motor", self.cali_dir_value)

    def dir_servo_angle_calibration(self, value):
        self.dir_cal_value = value
        self.config_flie.set("picarx_dir_servo", "%s" % value)
        self.dir_servo_pin.angle(value)

    def set_dir_servo_angle(self, value):
        self.dir_current_angle = value
        angle_value = value + self.dir_cal_value
        self.dir_servo_pin.angle(angle_value)

    def get_dir_current_angle(self):
        return self.dir_current_angle

    def camera_servo1_angle_calibration(self, value):
        self.cam_cal_value_1 = value
        self.config_flie.set("picarx_cam_servo1", "%s" % value)
        self.camera_servo_pin1.angle(value)

    def camera_servo2_angle_calibration(self, value):
        self.cam_cal_value_2 = value
        self.config_flie.set("picarx_cam_servo2", "%s" % value)
        self.camera_servo_pin2.angle(value)

    def set_camera_servo1_angle(self, value):
        self.camera_servo_pin1.angle(-1 * (value + -1 * self.cam_cal_value_1))

    def set_camera_servo2_angle(self, value):
        self.camera_servo_pin2.angle(-1 * (value + -1 * self.cam_cal_value_2))

    def set_power(self, speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    @log_on_error(logging.DEBUG, "Error in backward motion.")
    def backward(self, speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            if abs_current_angle > 40:
                abs_current_angle = 40

            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, -speed)
                self.set_motor_speed(2, self.turning_motor_speed(speed, abs_current_angle))
            else:
                self.set_motor_speed(1, -self.turning_motor_speed(speed, abs_current_angle))
                self.set_motor_speed(2, speed)
        else:
            self.set_motor_speed(1, -speed)
            self.set_motor_speed(2, speed)

    @log_on_error(logging.DEBUG, "Error in forward motion.")
    def forward(self, speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            if abs_current_angle > 40:
                abs_current_angle = 40

            # logging.debug(f"{speed}, {self.turning_motor_speed(speed, abs_current_angle)}")
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, speed)
                self.set_motor_speed(2, -self.turning_motor_speed(speed, abs_current_angle))
            else:
                self.set_motor_speed(1, self.turning_motor_speed(speed, abs_current_angle))
                self.set_motor_speed(2, -speed)

        else:
            self.set_motor_speed(1, speed)
            self.set_motor_speed(2, -speed)

    @log_on_error(logging.DEBUG, "Error with the turning motor speed")
    def turning_motor_speed(self, v_1, theta):
        v_2 = (
            (self.WIDTH_BACK_WHEELBASE / 2 + self.LENGTH_CHASSIS * 1 / np.tan(np.radians(theta)))
            / (self.LENGTH_CHASSIS * 1 / np.tan(np.radians(theta)) - self.WIDTH_BACK_WHEELBASE / 2)
        ) * v_1
        return v_2

    @log_on_end(logging.DEBUG, "PicarX motors stopped.")
    def stop(self):
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)

    def cleanup(self):
        self.stop()

    def get_distance(self):
        return self.ultrasonic.read()

    def set_grayscale_reference(self, value):
        self.get_grayscale_reference = value

    def get_grayscale_data(self):
        return list.copy(self.grayscale_sensor.get_grayscale_data())

    def get_line_status(self, gm_val_list):
        return str(self.grayscale_sensor.get_line_status(gm_val_list))

    def print_grayscale_data(self):
        data = self.get_grayscale_data()
        print(data)
        print(self.interpreter.follow_path(data))

    def follow_path(self):
        return

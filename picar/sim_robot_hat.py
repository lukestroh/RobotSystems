#!/usr/bin/python3
"""
sim_robot_hat.py
Luke Strohbehn
"""
from typing import Any
import math
import os
import time


class _Basic_class(object):
    _class_name = "_Basic_class"

    def __init__(self) -> None:
        pass

    @property
    def debug(self):
        pass

    @debug.setter
    def debug(self, debug):
        pass

    def run_command(self, cmd):
        import subprocess

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read().decode("utf-8")
        status = p.poll()
        return status, result

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Pin(_Basic_class):
    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0": 17,
        "D1": 18,
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,
        "D7": 4,
        "D8": 5,
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 19,
        "USER": 19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    _dict_2 = {
        "D0": 17,
        "D1": 4,  # Changed
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,  # Removed
        "D7": 4,  # Removed
        "D8": 5,  # Removed
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 25,  # Changed
        "USER": 25,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 5,  # Changed
    }

    def __init__(self, *value) -> None:
        super().__init__()

        if len(value) > 0:
            pin = value[0]
        if len(value) > 1:
            mode = value[1]
        else:
            mode = None
        if len(value) > 2:
            setup = value[2]
        else:
            setup = None
        if isinstance(pin, str):
            try:
                self._board_name = pin
                self._pin = self.dict()[pin]
            except Exception as e:
                print(e)
                # self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            self._pin = pin
        else:
            # self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
            pass
        self._value = 0
        self.init(mode, pull=setup)
        # self._info("Pin init finished.")
        pass

    def check_board_type(self) -> None:
        pass

    def init(self, mode, pull=None) -> None:
        self._pull = pull
        self._mode = mode
        pass

    def dict(self, *_dict) -> None:
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict
                )

    def __call__(self, value) -> Any:
        return self.value(value)

    def value(self, *value: Any) -> Any:
        if len(value) == 0:
            return 0
        else:
            value = value[0]
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        self.on()

    def low(self):
        self.off()

    def mode(self, *value):
        if len(value) == 0:
            return (self._mode, self._pull)
        else:
            pass

    def pull(self):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        pass

    def name(self):
        return f"GPIO{self._pin}"

    def names(self):
        return [self.name, self._board_name]


class Servo(_Basic_class):
    def __init__(self, pwm) -> None:
        pass

    def angle(self, angle) -> None:
        pass

    def set_pwm(self, pwm_value) -> None:
        pass


class fileDB(object):
    """A file based database.

    A file based database, read and write arguements in the specific file.
    """

    def __init__(self, db: str, mode: str = None, owner: str = None):
        self.db = db
        if self.db != None:
            self.file_check_create(db, mode, owner)
        else:
            raise ValueError("db: Missing file path parameter")

    def file_check_create(self, file_path: str, mode: str = None, owner: str = None):
        dir = file_path.rsplit("/", 1)[0]
        try:
            if os.path.exists(file_path):
                if not os.path.isfile(file_path):
                    print("Could not create file, there is a folder with the same name")
                    return
            else:
                if os.path.exists(dir):
                    if not os.path.isdir(dir):
                        print("Could not create directory, there is a file with the same name")
                        return
                else:
                    os.makedirs(file_path.rsplit("/", 1)[0], mode=0o754)
                    time.sleep(0.001)

                with open(file_path, "w") as f:
                    f.write("# robot-hat config and calibration value of robots\n\n")

            if mode != None:
                os.popen("sudo chmod %s %s" % (mode, file_path))
            if owner != None:
                os.popen("sudo chown -R %s:%s %s" % (owner, owner, file_path.rsplit("/", 1)[0]))
        except Exception as e:
            raise (e)

    def get(self, name, default_value=None):
        """Get value by data's name. Default value is for the arguemants do not exist"""
        try:
            conf = open(self.db, "r")
            lines = conf.readlines()
            conf.close()
            file_len = len(lines) - 1
            flag = False
            # Find the arguement and set the value
            for i in range(file_len):
                if lines[i][0] != "#":
                    if lines[i].split("=")[0].strip() == name:
                        value = lines[i].split("=")[1].replace(" ", "").strip()
                        flag = True
            if flag:
                return value
            else:
                return default_value
        except FileNotFoundError:
            conf = open(self.db, "w")
            conf.write("")
            conf.close()
            return default_value
        except:
            return default_value

    def set(self, name, value):
        """Set value by data's name. Or create one if the arguement does not exist"""

        # Read the file
        conf = open(self.db, "r")
        lines = conf.readlines()
        conf.close()
        file_len = len(lines) - 1
        flag = False
        # Find the arguement and set the value
        for i in range(file_len):
            if lines[i][0] != "#":
                if lines[i].split("=")[0].strip() == name:
                    lines[i] = "%s = %s\n" % (name, value)
                    flag = True
        # If arguement does not exist, create one
        if not flag:
            lines.append("%s = %s\n\n" % (name, value))

        # Save the file
        conf = open(self.db, "w")
        conf.writelines(lines)
        conf.close()


def _retry_wrapper(func):
    def wrapper(self, *arg, **kwargs):
        for i in range(self.RETRY):
            try:
                return func(self, *arg, **kwargs)
            except OSError:
                self._debug("OSError: %s" % func.__name__)
                continue
        else:
            return False

    return wrapper


class I2C(_Basic_class):
    def __init__(self, *args, **kargs) -> None:
        super().__init__()
        pass

    @_retry_wrapper
    def _i2c_write_byte(self, addr, data):  # i2C 写系列函数
        pass

    @_retry_wrapper
    def _i2c_write_byte_data(self, addr, reg, data):
        pass

    @_retry_wrapper
    def _i2c_write_word_data(self, addr, reg, data):
        pass

    @_retry_wrapper
    def _i2c_write_i2c_block_data(self, addr, reg, data):
        pass

    @_retry_wrapper
    def _i2c_read_byte(self, addr):  # i2C 读系列函数
        pass

    @_retry_wrapper
    def _i2c_read_i2c_block_data(self, addr, reg, num):
        pass

    @_retry_wrapper
    def is_ready(self, addr):
        pass

    def scan(self):  # 查看有哪些i2c设备
        pass

    def send(self, send, addr, timeout=0):  # 发送数据，addr为从机地址，send为数据
        pass

    def recv(self, recv, addr=0x00, timeout=0):  # 接收数据
        pass

    def mem_write(self, data, addr, memaddr, timeout=5000, addr_size=8):  # memaddr match to chn
        pass

    @_retry_wrapper
    def mem_read(self, data, addr, memaddr, timeout=5000, addr_size=8):  # 读取数据
        pass

    def readfrom_mem_into(self, addr, memaddr, buf):
        pass

    def writeto_mem(self, addr, memaddr, data):
        pass


timer = [{"arr": 0}] * 4


class PWM(I2C):
    REG_CHN = 0x20
    REG_FRE = 0x30
    REG_PSC = 0x40
    REG_ARR = 0x44

    ADDR = 0x14

    CLOCK = 72000000

    def __init__(self, channel, debug="critical") -> None:
        super().__init__()
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
                if channel > 14:
                    raise ValueError("channel must be in range of 0-14")
            else:
                raise ValueError("PWM channel should be between [P0, P11], not {0}".format(channel))
        try:
            self.send(0x2C, self.ADDR)
            self.send(0, self.ADDR)
            self.send(0, self.ADDR)
        except IOError:
            self.ADDR = 0x15

        self.debug = debug
        # self._debug("PWM address: {:02X}".format(self.ADDR))
        self.channel = channel
        self.timer = int(channel / 4)
        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def i2c_write(self, reg, value):
        pass

    def freq(self, *freq):
        if len(freq) == 0:
            return self._freq
        else:
            self._freq = int(freq[0])
            # [prescaler,arr] list
            result_ap = []
            # accuracy list
            result_acy = []
            # middle value for equal arr prescaler
            st = int(math.sqrt(self.CLOCK / self._freq))
            # get -5 value as start
            st -= 5
            # prevent negetive value
            if st <= 0:
                st = 1
            for psc in range(st, st + 10):
                arr = int(self.CLOCK / self._freq / psc)
                result_ap.append([psc, arr])
                result_acy.append(abs(self._freq - self.CLOCK / psc / arr))
            i = result_acy.index(min(result_acy))
            psc = result_ap[i][0]
            arr = result_ap[i][1]
            # self._debug("prescaler: %s, period: %s"%(psc, arr))
            self.prescaler(psc)
            self.period(arr)

    def prescaler(self, *prescaler):
        if len(prescaler) == 0:
            return self._prescaler
        else:
            self._prescaler = int(prescaler[0]) - 1
            reg = self.REG_PSC + self.timer
            # self._debug("Set prescaler to: %s"%self._prescaler)

    def period(self, *arr):
        global timer
        if len(arr) == 0:
            return timer[self.timer]["arr"]
        else:
            timer[self.timer]["arr"] = int(arr[0]) - 1
            reg = self.REG_ARR + self.timer
            # self._debug("Set arr to: %s"%timer[self.timer]["arr"])

    def pulse_width(self, *pulse_width):
        if len(pulse_width) == 0:
            return self._pulse_width
        else:
            self._pulse_width = int(pulse_width[0])
            reg = self.REG_CHN + self.channel

    def pulse_width_percent(self, *pulse_width_percent):
        global timer
        if len(pulse_width_percent) == 0:
            return self._pulse_width_percent
        else:
            self._pulse_width_percent = pulse_width_percent[0]
            temp = self._pulse_width_percent / 100.0
            # print(temp)
            pulse_width = temp * timer[self.timer]["arr"]
            self.pulse_width(pulse_width)


class ADC(I2C):
    ADDR = 0x14  # 扩展板的地址为0x14

    def __init__(self, chn):  # 参数，通道数，树莓派扩展板上有8个adc通道分别为"A0, A1, A2, A3, A4, A5, A6, A7"
        super().__init__()
        if isinstance(chn, str):
            if chn.startswith("A"):  # 判断穿境来的参数是否为A开头，如果是，取A后面的数字出来
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:  # 判断取出来的数字是否在0~7的范围内
            self._error("Incorrect channel range")
        chn = 7 - chn
        self.chn = chn | 0x10  # 给从机地址
        self.reg = 0x40 + self.chn

    def read(self):
        value = 0b10000001
        return value

    def read_voltage(self):
        return self.read * 3.3 / 4095


class Ultrasonic:
    def __init__(self, trig, echo, timeout=0.02):
        self.trig = trig
        self.echo = echo
        self.timeout = timeout

    def _read(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value() == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value() == 1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, times=10):
        for i in range(times):
            a = self._read()
            if a != -1:
                return a
        return -1


class Grayscale_Module(object):
    def __init__(self, pin0, pin1, pin2, reference=1000):
        self.chn_0 = ADC(pin0)
        self.chn_1 = ADC(pin1)
        self.chn_2 = ADC(pin2)
        self.reference = reference

    def get_line_status(self, fl_list):
        if fl_list[0] > self.reference and fl_list[1] > self.reference and fl_list[2] > self.reference:
            return "stop"

        elif fl_list[1] <= self.reference:
            return "forward"

        elif fl_list[0] <= self.reference:
            return "right"

        elif fl_list[2] <= self.reference:
            return "left"

    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

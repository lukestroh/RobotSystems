#!/usr/bin/env/python3
"""
motors.py
Luke Strohbehn
"""
from picar.utils.basic import _Basic_class
from picar.sensor import I2C
import RPi.GPIO as GPIO
import smbus


class Pin(_Basic_class):
    def __init__(self, *value):
        super().__init__()
        # Pin
        self.OUT = GPIO.OUT
        self.IN = GPIO.IN
        self.IRQ_FALLING = GPIO.FALLING
        self.IRQ_RISING = GPIO.RISING
        self.IRQ_RISING_FALLING = GPIO.BOTH
        self.PULL_UP = GPIO.PUD_UP
        self.PULL_DOWN = GPIO.PUD_DOWN
        self.PULL_NONE = None

        self._dict = {
            "BOARD_TYPE": 12,
        }

        self._dict_1 = {
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

        self._dict_2 = {
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.check_board_type()

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
                self._error("Pin should be in %s, not %s" % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            self._pin = pin
        else:
            self._error("Pin should be in %s, not %s" % (self._dict.keys(), pin))
        self._value = 0
        self.init(mode, pull=setup)
        self._info("Pin init finished.")

    def check_board_type(self):
        type_pin = self.dict()["BOARD_TYPE"]
        GPIO.setup(type_pin, GPIO.IN)
        if GPIO.input(type_pin) == 0:
            self._dict = self._dict_1
        else:
            self._dict = self._dict_2

    def init(self, mode, pull=PULL_NONE):
        self._pull = pull
        self._mode = mode
        if mode != None:
            if pull != None:
                GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                GPIO.setup(self._pin, mode)

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict
                )

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            if self._mode in [None, self.OUT]:
                self.mode(self.IN)
            result = GPIO.input(self._pin)
            self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:
            value = value[0]
            if self._mode in [None, self.IN]:
                self.mode(self.OUT)
            GPIO.output(self._pin, value)
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return (self._mode, self._pull)
        else:
            self._mode = value[0]
            if len(value) == 1:
                GPIO.setup(self._pin, self._mode)
            elif len(value) == 2:
                self._pull = value[1]
                GPIO.setup(self._pin, self._mode, self._pull)

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)
        GPIO.add_event_detect(self._pin, trigger, callback=handler, bouncetime=bouncetime)

    def name(self):
        return "GPIO%s" % self._pin

    def names(self):
        return [self.name, self._board_name]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4 = 4
        GPIO5 = 5
        GPIO6 = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass

def _retry_wrapper(self, func):
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



class PWM(I2C):
    def __init__(self, channel, debug="critical"):
        super().__init__()
        # PWM
        self.REG_CHN = 0x20
        self.REG_FRE = 0x30
        self.REG_PSC = 0x40
        self.REG_ARR = 0x44
        self.ADDR = 0x14
        self.CLOCK = 72000000

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
        self._debug("PWM address: {:02X}".format(self.ADDR))
        self.channel = channel
        self.timer = int(channel / 4)
        self.bus = smbus.SMBus(1)
        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def i2c_write(self, reg, value):
        value_h = value >> 8
        value_l = value & 0xFF
        self._debug("i2c write: [0x%02X, 0x%02X, 0x%02X, 0x%02X]" % (self.ADDR, reg, value_h, value_l))
        # print("i2c write: [0x%02X, 0x%02X, 0x%02X] to 0x%02X"%(reg, value_h, value_l, self.ADDR))
        self.send([reg, value_h, value_l], self.ADDR)

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
            self._debug("prescaler: %s, period: %s" % (psc, arr))
            self.prescaler(psc)
            self.period(arr)

    def prescaler(self, *prescaler):
        if len(prescaler) == 0:
            return self._prescaler
        else:
            self._prescaler = int(prescaler[0]) - 1
            reg = self.REG_PSC + self.timer
            self._debug("Set prescaler to: %s" % self._prescaler)
            self.i2c_write(reg, self._prescaler)

    def period(self, *arr):
        # global timer
        if len(arr) == 0:
            return timer[self.timer]["arr"]
        else:
            timer[self.timer]["arr"] = int(arr[0]) - 1
            reg = self.REG_ARR + self.timer
            self._debug("Set arr to: %s" % timer[self.timer]["arr"])
            self.i2c_write(reg, timer[self.timer]["arr"])

    def pulse_width(self, *pulse_width):
        if len(pulse_width) == 0:
            return self._pulse_width
        else:
            self._pulse_width = int(pulse_width[0])
            reg = self.REG_CHN + self.channel
            self.i2c_write(reg, self._pulse_width)

    def pulse_width_percent(self, *pulse_width_percent):
        # global timer
        if len(pulse_width_percent) == 0:
            return self._pulse_width_percent
        else:
            self._pulse_width_percent = pulse_width_percent[0]
            temp = self._pulse_width_percent / 100.0
            # print(temp)
            pulse_width = temp * timer[self.timer]["arr"]
            self.pulse_width(pulse_width)

class Servo(_Basic_class):
    def __init__(self, pwm):
        super().__init__()
        
        # Servo
        self.MAX_PW = 2500
        self.MIN_PW = 500
        self._freq = 50
        self.pwm = pwm
        self.pwm.period(4095)
        prescaler = int(float(self.pwm.CLOCK) / self.pwm._freq / self.pwm.period())
        self.pwm.prescaler(prescaler)
        # self.angle(90)

    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        if not (isinstance(angle, int) or isinstance(angle, float)):
            raise ValueError("Angle value should be int or float value, not %s" % type(angle))
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        High_level_time = self.map(angle, -90, 90, self.MIN_PW, self.MAX_PW)
        self._debug("High_level_time: %f" % High_level_time)
        pwr = High_level_time / 20000
        self._debug("pulse width rate: %f" % pwr)
        value = int(pwr * self.pwm.period())
        self._debug("pulse width value: %d" % value)
        self.pwm.pulse_width(value)

    # pwm_value ranges MIN_PW 500 to MAX_PW 2500 degrees
    def set_pwm(self, pwm_value):
        if pwm_value > self.MAX_PW:
            pwm_value = self.MAX_PW
        if pwm_value < self.MIN_PW:
            pwm_value = self.MIN_PW

        self.pwm.pulse_width(pwm_value)

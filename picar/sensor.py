#!/usr/bin/env/python3
"""
sensors.py
Luke Strohbehn
"""
from picar.utils.basic import _Basic_class

# from motor import Motor
import time
from picar.utils.bus import GrayscaleBus, UltrasonicBus
from typing import Any

from smbus import SMBus


class I2C(_Basic_class):
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

    def __init__(self, *args, **kargs):  # *args表示位置参数（形式参数），可无，； **kargs表示默认值参数，可无。
        super().__init__()
        self._bus = 1
        self._smbus = SMBus(self._bus)

        # I2C
        self.MASTER = 0
        self.SLAVE = 1
        self.RETRY = 5

    @_retry_wrapper
    def _i2c_write_byte(self, addr, data):  # i2C 写系列函数
        self._debug("_i2c_write_byte: [0x{:02X}] [0x{:02X}]".format(addr, data))
        result = self._smbus.write_byte(addr, data)
        return result

    @_retry_wrapper
    def _i2c_write_byte_data(self, addr, reg, data):
        self._debug("_i2c_write_byte_data: [0x{:02X}] [0x{:02X}] [0x{:02X}]".format(addr, reg, data))
        return self._smbus.write_byte_data(addr, reg, data)

    @_retry_wrapper
    def _i2c_write_word_data(self, addr, reg, data):
        self._debug("_i2c_write_word_data: [0x{:02X}] [0x{:02X}] [0x{:04X}]".format(addr, reg, data))
        return self._smbus.write_word_data(addr, reg, data)

    @_retry_wrapper
    def _i2c_write_i2c_block_data(self, addr, reg, data):
        self._debug("_i2c_write_i2c_block_data: [0x{:02X}] [0x{:02X}] {}".format(addr, reg, data))
        return self._smbus.write_i2c_block_data(addr, reg, data)

    @_retry_wrapper
    def _i2c_read_byte(self, addr):  # i2C 读系列函数
        self._debug("_i2c_read_byte: [0x{:02X}]".format(addr))
        return self._smbus.read_byte(addr)

    @_retry_wrapper
    def _i2c_read_i2c_block_data(self, addr, reg, num):
        self._debug("_i2c_read_i2c_block_data: [0x{:02X}] [0x{:02X}] [{}]".format(addr, reg, num))
        return self._smbus.read_i2c_block_data(addr, reg, num)

    @_retry_wrapper
    def is_ready(self, addr):
        addresses = self.scan()
        if addr in addresses:
            return True
        else:
            return False

    def scan(self):  # 查看有哪些i2c设备
        cmd = "i2cdetect -y %s" % self._bus
        _, output = self.run_command(cmd)  # 调用basic中的方法，在linux中运行cmd指令，并返回运行后的内容

        outputs = output.split("\n")[1:]  # 以回车符为分隔符，分割第二行之后的所有行
        self._debug("outputs")
        addresses = []
        for tmp_addresses in outputs:
            if tmp_addresses == "":
                continue
            tmp_addresses = tmp_addresses.split(":")[1]
            tmp_addresses = tmp_addresses.strip().split(" ")  # strip函数是删除字符串两端的字符，split函数是分隔符
            for address in tmp_addresses:
                if address != "--":
                    addresses.append(int(address, 16))
        self._debug("Conneceted i2c device: %s" % addresses)  # append以列表的方式添加address到addresses中
        return addresses

    def send(self, send, addr, timeout=0):  # 发送数据，addr为从机地址，send为数据
        if isinstance(send, bytearray):
            data_all = list(send)
        elif isinstance(send, int):
            data_all = []
            d = "{:X}".format(send)
            d = "{}{}".format(
                "0" if len(d) % 2 == 1 else "", d
            )  # format是将()中的内容对应填入{}中，（）中的第一个参数是一个三目运算符，if条件成立则为“0”，不成立则为“”(空的意思)，第二个参数是d，此行代码意思为，当字符串为奇数位时，在字符串最强面添加‘0’，否则，不添加， 方便以下函数的应用
            # print(d)
            for i in range(len(d) - 2, -1, -2):  # 从字符串最后开始取，每次取2位
                tmp = int(d[i : i + 2], 16)  # 将两位字符转化为16进制
                # print(tmp)
                data_all.append(tmp)  # 添加到data_all数组中
            data_all.reverse()
        elif isinstance(send, list):
            data_all = send
        else:
            raise ValueError("send data must be int, list, or bytearray, not {}".format(type(send)))

        if len(data_all) == 1:  # 如果data_all只有一组数
            data = data_all[0]
            # print("i2c write: [0x%02X] to 0x%02X"%(data, addr))
            self._i2c_write_byte(addr, data)
        elif len(data_all) == 2:  # 如果data_all只有两组数
            reg = data_all[0]
            data = data_all[1]
            self._i2c_write_byte_data(addr, reg, data)
        elif len(data_all) == 3:  # 如果data_all只有三组数
            reg = data_all[0]
            data = (data_all[2] << 8) + data_all[1]
            self._i2c_write_word_data(addr, reg, data)
        else:
            reg = data_all[0]
            data = list(data_all[1:])
            self._i2c_write_i2c_block_data(addr, reg, data)

    def recv(self, recv, addr=0x00, timeout=0):  # 接收数据
        if isinstance(recv, int):  # 将recv转化为二进制数
            result = bytearray(recv)
        elif isinstance(recv, bytearray):
            result = recv
        else:
            return False
        for i in range(len(result)):
            result[i] = self._i2c_read_byte(addr)
        return result

    def mem_write(self, data, addr, memaddr, timeout=5000, addr_size=8):  # memaddr match to chn
        if isinstance(data, bytearray):
            data_all = list(data)
        elif isinstance(data, list):
            data_all = data
        elif isinstance(data, int):
            data_all = []
            data = "%x" % data
            if len(data) % 2 == 1:
                data = "0" + data
            # print(data)
            for i in range(0, len(data), 2):
                # print(data[i:i+2])
                data_all.append(int(data[i : i + 2], 16))
        else:
            raise ValueError("memery write require arguement of bytearray, list, int less than 0xFF")
        # print(data_all)
        self._i2c_write_i2c_block_data(addr, memaddr, data_all)

    @_retry_wrapper
    def mem_read(self, data, addr, memaddr, timeout=5000, addr_size=8):  # 读取数据
        if isinstance(data, int):
            num = data
        elif isinstance(data, bytearray):
            num = len(data)
        else:
            return False
        result = bytearray(self._i2c_read_i2c_block_data(addr, memaddr, num))
        return result

    def readfrom_mem_into(self, addr, memaddr, buf):
        buf = self.mem_read(len(buf), addr, memaddr)
        return buf

    def writeto_mem(self, addr, memaddr, data):
        self.mem_write(data, addr, memaddr)


class ADC(I2C):
    def __init__(self, chn):  # 参数，通道数，树莓派扩展板上有8个adc通道分别为"A0, A1, A2, A3, A4, A5, A6, A7"
        super().__init__()
        self.ADDR = 0x14
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
        # self.bus = smbus.SMBus(1)

    def read(self):  # adc通道读取数---写一次数据，读取两次数据 （读取的数据范围是0~4095）
        self._debug("Write 0x%02X to 0x%02X" % (self.chn, self.ADDR))
        # self.bus.write_byte(self.ADDR, self.chn)      # 写入数据
        self.send([self.chn, 0, 0], self.ADDR)

        self._debug("Read from 0x%02X" % (self.ADDR))
        # value_h = self.bus.read_byte(self.ADDR)
        value_h = self.recv(1, self.ADDR)[0]  # 读取数据

        self._debug("Read from 0x%02X" % (self.ADDR))
        # value_l = self.bus.read_byte(self.ADDR)
        value_l = self.recv(1, self.ADDR)[0]  # 读取数据（读两次）

        value = (value_h << 8) + value_l
        self._debug("Read value: %s" % value)
        return value

    def read_voltage(self):  # 将读取的数据转化为电压值（0~3.3V）
        return self.read * 3.3 / 4095


class UltrasonicSensor:
    def __init__(self, px, trig, echo, timeout=0.02):
        self.trig = trig
        self.echo = echo
        self.timeout = timeout
        px.interpreter_bus = UltrasonicBus()
        self.interpreter_bus = px.interpreter_bus

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

    def write_interpreter_bus(self, message: Any):
        return self.interpreter_bus.write(message)

    def run(self, time_delay: float):
        while True:
            self.interpreter_bus.write(self.read())
            time.sleep(time_delay)


class GrayscaleSensor:
    def __init__(self, px, pin0, pin1, pin2, reference=1000):
        self.chn_0 = ADC(pin0)
        self.chn_1 = ADC(pin1)
        self.chn_2 = ADC(pin2)
        self.reference = reference
        px.grayscale_bus = GrayscaleBus()
        self.grayscale_bus = px.grayscale_bus

    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

    def write_interpreter_bus(self, message: Any):
        return self.grayscale_bus.write(message)

    def run(self, time_delay: float):
        while True:
            self.write_interpreter_bus(self.get_grayscale_data())
            time.sleep(time_delay)


def main():
    grayscale_pins: list = ["A0", "A1", "A2"]

    greyscale = GrayscaleSensor(grayscale_pins[0], grayscale_pins[1], grayscale_pins[2])
    # ultrasonic = Ultrasonic()
    return


if __name__ == "__main__":
    main()

import time
import Board
import signal

print(
    """
**********************************************************
******Magic Er Technology Raspberry Pi expansion board****
***********RGB light control routine**********************
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
----------------------------------------------------------
The following commands can be used in the LX terminal,
which can be opened by ctrl+alt+t, or click on the 
black LX terminal icon on the upper bar.
----------------------------------------------------------
Usage:
    sudo python3 RGBControlDemo.py
----------------------------------------------------------
Version: --V1.0  2020/08/12
----------------------------------------------------------
Tips:
 * Press ctrl+c to close this program, if it fails,
 please try again!
----------------------------------------------------------
"""
)

start = True


# 关闭前处理
def Stop(signum, frame):
    global start

    start = False
    print("Closing...")


# 先将所有灯关闭
Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
Board.RGB.show()

signal.signal(signal.SIGINT, Stop)

while True:
    # 设置2个灯为红色
    Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
    Board.RGB.show()
    time.sleep(1)

    # 设置2个灯为绿色
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
    Board.RGB.show()
    time.sleep(1)

    # 设置2个灯为蓝色
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
    Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
    Board.RGB.show()
    time.sleep(1)

    # 设置2个灯为黄色
    Board.RGB.setPixelColor(0, Board.PixelColor(255, 255, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(255, 255, 0))
    Board.RGB.show()
    time.sleep(1)

    if not start:
        # 所有灯关闭
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()
        print("closed")
        break

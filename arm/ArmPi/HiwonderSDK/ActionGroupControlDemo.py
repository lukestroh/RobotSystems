import time
import Board
import ActionGroupControl as AGC

print(
    """
**********************************************************
*********功能:幻尔科技树莓派扩展板，动作组控制例程********
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
----------------------------------------------------------
以下指令均需在LX终端使用，LX终端可通过ctrl+alt+t打开，或点
击上栏的黑色LX终端图标。
----------------------------------------------------------
Usage:
    sudo python3 ActionGroupControlDemo.py
----------------------------------------------------------
Version: --V1.0  2020/08/12
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
"""
)

# 动作组需要保存在路径/home/pi/ArmPi/ActionGroups下
AGC.runAction("1")  # 参数为动作组的名称，不包含后缀，以字符形式传入
AGC.runAction("2")
# AGC.runAction('calibration')
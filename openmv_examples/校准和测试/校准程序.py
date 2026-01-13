# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

import Robot_arm as rb        # 机械臂控制模块
import time
# 初始化机械臂和显示屏
robot = rb.Robot(3)           # 创建机械臂对象，串口3用于通信
time.sleep_ms(1000)
robot.Servo(0)
time.sleep_ms(1000)
robot.Set_Endstep(900,1800,3780,0) #设置机械臂复位时旋转的角度（此程序每个机械臂只需要运行一遍即可，后续若需要更改复位参数再调用运行）
time.sleep_ms(1000)
# robot.home_setting()         # 机械臂复位

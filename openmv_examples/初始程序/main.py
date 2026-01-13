# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

# 导入所需模块
import sensor, image           # 摄像头和图像处理模块
import display                # 显示屏驱动模块
import Robot_arm as rb        # 机械臂控制模块

# 初始化摄像头
sensor.reset()                # 重置摄像头传感器
sensor.set_pixformat(sensor.RGB565)  # 设置像素格式为RGB565（也可用GRAYSCALE灰度）
sensor.set_framesize(sensor.QQVGA)   # 设置帧大小为QQVGA（128x160），适配LCD屏幕
sensor.skip_frames(time=2000)        # 跳过前2000ms的帧，等待摄像头稳定

# 初始化机械臂和显示屏
robot = rb.Robot(3)           # 创建机械臂对象，串口3用于通信(H7 H7P)
# robot = rb.Robot(1)           # 创建机械臂对象，串口1用于通信(RT)
# robot.Set_Endstep(900,1800,3780,0) #设置机械臂复位时旋转的角度
lcd = display.SPIDisplay()    # 创建SPI显示屏对象
# robot.home_setting()         # 机械臂复位，若异常需重启机械臂后再运行

# 获取并打印机械臂当前坐标
# a = robot.get_xyz_point()     # 获取机械臂当前XYZE坐标
# print(f"X:{int(a[0])} Y:{int(a[1])} Z:{int(a[2])}")  # 打印坐标信息

# 其他机械臂功能示例（可根据需要取消注释使用）
# robot.get_key_val()         # 获取按键值
# robot.set_xyz_point(0,174,277,0,0)    # 设置机械臂目标坐标（X,Y,Z,E,F）
#                                     # E为滑轨坐标，无滑轨填0，F为速度，<5自动插值
#                                     # x=0,y=174,z=277为复位初始坐标
robot.relay(True)          # 控制机械臂主板继电器
# robot.Servo(0)             # 控制主板舵机

# 主循环，持续运行
while True:
    img = sensor.snapshot()                  # 拍摄一帧图像
    key = robot.ad_key_control()                   # 通过AD按键控制机械臂
    if key != 0:
        print(key)
    img.draw_string(0,0, "Hello Robot!",color=(255,0,0))  # 在图像上显示欢迎语
    lcd.write(img.copy(hint=image.ROTATE_90))            # 图像旋转90度后写入LCD显示屏

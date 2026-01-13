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
robot = rb.Robot(3)           # 创建机械臂对象，串口3用于通信
# robot.Set_Endstep(900,1800,3780,0) #设置机械臂复位时旋转的角度
lcd = display.SPIDisplay()    # 创建SPI显示屏对象
robot.home_setting()         # 机械臂复位，若异常需重启机械臂后再运行

# 舵机初始角度和机械臂空间坐标
angle = 45   # 舵机初始角度
X = 0        # X轴初始坐标
Y = 174      # Y轴初始坐标
Z = 290      # Z轴初始坐标

# 通过AD按键控制机械臂
def key_control():
    global angle, X, Y, Z
    key = robot.ad_key_control()
    if key != 0:
        print(key)
        if key == 1:
            angle = angle + 5
            robot.Servo(angle)
            robot.relay(True)
        elif key == 7:
            angle = angle - 5
            robot.Servo(angle)
            robot.relay(False)
        elif key == 2:
            X = X - 5
            robot.set_xyz_point(X,Y,Z,0,0)
        elif key == 8:
            X = X + 5
            robot.set_xyz_point(X,Y,Z,0,0)
        elif key == 4:
            Y = Y + 5
            robot.set_xyz_point(X,Y,Z,0,0)
        elif key == 6:
            Y = Y - 5
            robot.set_xyz_point(X,Y,Z,0,0)
        elif key == 9:
            Z = Z + 5
            robot.set_xyz_point(X,Y,Z,0,0)
        elif key == 3:
            Z = Z - 5
            robot.set_xyz_point(X,Y,Z,0,0)
        elif key == 5:
            robot.home_setting()
            angle = 45
            X = 0
            Y = 174
            Z = 290

while True:
    img = sensor.snapshot()                  # 拍摄一帧图像
    key_control()
    a = robot.get_xyz_point()     # 获取机械臂当前XYZE坐标
    img.draw_string(0,0, "Hello Robot!",color=(255,0,0))  # 在图像上显示欢迎语
    img.draw_string(0,10,f"X:{int(a[0])} Y:{int(a[1])} Z:{int(a[2])}",color=(255,0,0))
    lcd.write(img.copy(hint=image.ROTATE_90))            # 图像旋转90度后写入LCD显示屏

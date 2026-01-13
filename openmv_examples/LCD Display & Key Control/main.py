# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com


"""
主控程序：LCD 显示与按键控制机械臂

功能说明：
- 使用摄像头采集图像并在 SPI LCD 上显示（适用于 OpenMV 平台）
- 通过 AD 按键（通过 `robot.ad_key_control()` 读取）对机械臂进行手动微调：
  - 控制舵机夹爪角度
  - 控制机械臂在 XYZ 空间的增量移动
  - 快速复位回到预设初始位置

说明：文件是在 OpenMV/微控制器环境下运行，依赖 `sensor`, `image`, `display`, `Robot_arm` 模块。
在本地编辑器会出现这些模块无法解析的提示，这是正常的。
"""

import sensor, image           # OpenMV 摄像头与图像处理模块
import display                # LCD/显示屏驱动模块
import Robot_arm as rb        # 项目内的机械臂控制模块


# ---------------- 摄像头初始化 ----------------
sensor.reset()                # 重置摄像头传感器
sensor.set_pixformat(sensor.RGB565)  # 使用 RGB565 彩色格式；需要灰度可改为 GRAYSCALE
sensor.set_framesize(sensor.QQVGA)   # 使用 QQVGA (128x160)，适配小 LCD
sensor.skip_frames(time=2000)        # 等待摄像头稳定（单位 ms）


# ---------------- 硬件初始化 ----------------
robot = rb.Robot(3)           # 创建机械臂对象，参数为串口号（按板子选择）
# 若使用另一串口/板子可改为 rb.Robot(1)
# robot.home_setting()        # 若需上电即复位，取消注释
lcd = display.SPIDisplay()    # 初始化 SPI LCD 显示对象


# ---------------- 全局控制参数 ----------------
# 舵机初始角度（夹爪角度）
angle = 45
# 机械臂初始空间坐标（可视具体机械臂标定调整）
X = 0
Y = 174
Z = 290

# 每次按键调整的增量（单位为机械臂坐标/角度的原脚本单位）
XYZ_LEN = 10    # XYZ 坐标移动步长
Servo_LEN = 5   # 舵机角度步长


def key_control():
    """读取 AD 按键并根据按键值调整机械臂状态。

    按键映射（根据 `robot.ad_key_control()` 返回值）：
    - 1: 舵机角度 +Servo_LEN（夹爪闭合或增加角度）
    - 7: 舵机角度 -Servo_LEN（夹爪张开或减少角度）
    - 2: X - XYZ_LEN
    - 8: X + XYZ_LEN
    - 4: Y + XYZ_LEN
    - 6: Y - XYZ_LEN
    - 9: Z + XYZ_LEN
    - 3: Z - XYZ_LEN
    - 5: 复位：调用 `robot.home_setting()` 并将角度/坐标恢复预设值

    函数通过 `robot.Servo()` 和 `robot.set_xyz_point()` 发送具体命令。
    """
    global angle, X, Y, Z
    key = robot.ad_key_control()
    if key != 0:
        # 打印按键以便调试（串口输出）
        print(key)
        if key == 1:
            angle = angle + Servo_LEN
            robot.Servo(angle)
        elif key == 7:
            angle = angle - Servo_LEN
            robot.Servo(angle)
        elif key == 2:
            X = X - XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 8:
            X = X + XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 4:
            Y = Y + XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 6:
            Y = Y - XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 9:
            Z = Z + XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 3:
            Z = Z - XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 5:
            # 复位到初始位置并恢复参数
            robot.home_setting()
            angle = 45
            X = 0
            Y = 174
            Z = 290


# ---------------- 主循环：采集显示并响应按键 ----------------
while True:
    img = sensor.snapshot()                  # 捕获一帧图像
    key_control()                            # 处理按键输入并发送控制命令

    # 从机械臂查询当前坐标（返回值通常为包含 X,Y,Z,E 的元组或列表）
    a = robot.get_xyz_point()

    # 在图像上绘制文字信息，便于 LCD 显示当前坐标
    img.draw_string(0, 0, "Hello Robot!", color=(255, 0, 0))
    img.draw_string(0, 10, f"X:{int(a[0])} Y:{int(a[1])} Z:{int(a[2])}", color=(255, 0, 0))

    # 将图像按 90 度旋转后写入 LCD（根据屏幕方向可调整）
    lcd.write(img.copy(hint=image.ROTATE_90))

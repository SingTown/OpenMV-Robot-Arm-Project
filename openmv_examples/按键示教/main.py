# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

"""主控程序：按键示教演示

功能概要：
- 使用摄像头采集图像并在LCD上显示实时画面和机械臂状态。
- 通过 AD 按键对机械臂进行手动控制（调整舵机角度、XYZ 坐标）。
- 支持保存当前点位到示教序列，并在检测到重复保存时触发回放。

说明：此文件运行在 OpenMV 平台，依赖平台提供的 `sensor`, `image`,
`display` 等模块以及工程中的 `Robot_arm` 驱动模块。
"""

# 导入所需模块
import sensor, image           # 摄像头和图像处理模块
import time
import display                # 显示屏驱动模块
import Robot_arm as rb        # 机械臂控制模块

# 初始化摄像头
sensor.reset()                # 重置摄像头传感器
sensor.set_pixformat(sensor.RGB565)  # 设置像素格式为RGB565（也可用GRAYSCALE灰度）
sensor.set_framesize(sensor.QQVGA)   # 设置帧大小为QQVGA（128x160），适配LCD屏幕
sensor.skip_frames(time=2000)        # 跳过前2000ms的帧，等待摄像头稳定

# 初始化机械臂和显示屏
# 通过传入串口号创建机械臂控制对象：参数取决于硬件接线（H7/H7P 常用 3）
robot = rb.Robot(3)
# 如果使用不同的串口，请取消下面一行注释并调整端口号
# robot = rb.Robot(1)
# 复位机械臂到初始安全位（执行一次回到默认舵机角度和坐标）
robot.home_setting()
# 初始化 SPI LCD 显示对象，用于把 camera 捕获画面输出到屏幕
lcd = display.SPIDisplay()

# 舵机初始角度和机械臂空间坐标
angle = 45   # 夹爪或目标舵机的初始角度（度数）
X = 0        # 机械臂初始 X 坐标（单位与 Robot_arm 驱动一致）
Y = 174      # 初始 Y 坐标，通常为平台相对值
Z = 290      # 初始 Z 坐标，代表臂长或高度

XYZ_LEN = 10  # 每次按键在 XYZ 轴上移动的增量（单位同坐标）
Servo_LEN = 5 # 每次按键在舵机角度上的增量（度）

# 示教存储点列表，每个点为 (X, Y, Z, angle)
positions = []


def is_same_point(p1, p2, pos_tol=1.0, angle_tol=5.0):
    """判断两个保存点是否相同（允许一定容差）
    p1/p2: (X, Y, Z, angle)
    pos_tol: 位置容差（单位同坐标）
    angle_tol: 角度容差（度）
    """
    if p1 is None or p2 is None:
        return False
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    dz = abs(p1[2] - p2[2])
    da = abs(p1[3] - p2[3])
    return dx <= pos_tol and dy <= pos_tol and dz <= pos_tol and da <= angle_tol


def playback_positions():
    """回放保存的示教点：先回到初始点，再按保存顺序回放。

    回放逻辑：
    - 如果没有保存点则直接返回。
    - （可选）先复位机械臂到默认位置，再依次移动到每个保存点并设置舵机角度。
    - 每个点移动后休眠以保证机械臂有足够时间完成动作。
    """
    global angle, X, Y, Z, positions
    if len(positions) == 0:
        print("没有保存的示教点，无法回放。")
        return
    print("示教前回到初始点...")
    # robot.home_setting()#可选择：在回放前执行复位
    robot.set_xyz_point(0, 174, 290, 0, 0)
    print("开始示教，回放 %d 个点" % len(positions))
    for idx, p in enumerate(positions):
        x, y, z, a_servo = p
        print("回放点 %d: %s" % (idx+1, str(p)))
        robot.set_xyz_point(x, y, z, 0, 0)
        try:
            robot.Servo(int(a_servo))
        except Exception:
            pass
        # 等待一段时间再到下一个点，确保机械臂有时间运动
        time.sleep_ms(800)

# 通过 AD 按键控制机械臂（key 值由底层驱动 `robot.ad_key_control()` 返回）
def key_control():
    """读取按键并根据按键编号调整舵机或 XYZ 坐标。

    按键映射（根据驱动返回值）：
    - 1: 舵机角度增加（+Servo_LEN）
    - 7: 舵机角度减少（-Servo_LEN）
    - 2: X 轴减少（向左或后退，-XYZ_LEN）
    - 8: X 轴增加（向右或前进，+XYZ_LEN）
    - 4: Y 轴增加（+XYZ_LEN）
    - 6: Y 轴减少（-XYZ_LEN）
    - 9: Z 轴增加（+XYZ_LEN）
    - 3: Z 轴减少（-XYZ_LEN）
    - 5: 保存当前位置到示教点列表（触发保存与可能的回放）
    """
    global angle, X, Y, Z
    key = robot.ad_key_control()
    if key != 0:
        print(key)
        if key == 1:
            # 增加舵机角度并应用
            angle = angle + Servo_LEN
            robot.Servo(angle)
        elif key == 7:
            # 减小舵机角度并应用
            angle = angle - Servo_LEN
            robot.Servo(angle)
        elif key == 2:
            # X 轴向负方向移动
            X = X - XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 8:
            # X 轴向正方向移动
            X = X + XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 4:
            # Y 轴向正方向移动
            Y = Y + XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 6:
            # Y 轴向负方向移动
            Y = Y - XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 9:
            # Z 轴向上（增加）移动
            Z = Z + XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 3:
            # Z 轴向下（减少）移动
            Z = Z - XYZ_LEN
            robot.set_xyz_point(X, Y, Z, 0, 0)
        elif key == 5:
            # 保存当前位置到示教点列表
            cur = robot.get_xyz_point()
            # 使用当前程序维护的 angle 作为夹爪角度
            saved = (float(cur[0]), float(cur[1]), float(cur[2]), float(angle))
            positions.append(saved)
            print("位置已保存：", saved, " 共计:", len(positions))
            # 如果连续两个保存点相同则删除前一个重复点，再触发回放
            if len(positions) >= 2 and is_same_point(positions[-1], positions[-2]):
                positions.pop(-2)  # 删除前一个重复的点，保留最新保存的点
                print("开始回放")
                playback_positions()

while True:
    img = sensor.snapshot()                  # 拍摄一帧图像
    key_control()
    a = robot.get_xyz_point()     # 获取机械臂当前XYZE坐标
    img.draw_string(0,0, "Hello Robot!",color=(255,0,0))  # 在图像上显示欢迎语
    img.draw_string(0,10,f"X:{int(a[0])} Y:{int(a[1])} Z:{int(a[2])}",color=(255,0,0))
    img.draw_string(0,20, f"保存点:{len(positions)}", color=(255,0,0))# 在图像上显示已保存的位置数量
    lcd.write(img.copy(hint=image.ROTATE_90))            # 图像旋转90度后写入LCD显示屏
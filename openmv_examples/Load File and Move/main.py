# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

"""
示例主程序：读取摄像头、显示图像并从文本文件执行机械臂运动指令。

说明：
- 本脚本运行于 OpenMV 环境（或类似支持 `sensor`, `image`, `display` 的平台）。
- 机械臂控制封装在 `Robot_arm` 模块（导入为 `rb`），通过串口发送指令。
"""

# 导入所需模块（OpenMV 风格）
import sensor, image           # 摄像头和图像处理模块
import display                # 显示屏驱动模块
import Robot_arm as rb        # 机械臂控制模块（本工程中的 Robot_arm.py）
import time


# ----------------------- 摄像头初始化 -----------------------
sensor.reset()                # 重置摄像头传感器
sensor.set_pixformat(sensor.RGB565)  # 使用 RGB565 彩色格式；若只需灰度可改为 GRAYSCALE
sensor.set_framesize(sensor.QQVGA)   # 使用 QQVGA 分辨率，适配小型 LCD（128x160 或类似）
sensor.skip_frames(time=2000)        # 等待摄像头稳定，跳过初始帧（单位 ms）


# ----------------------- 机械臂与显示屏初始化 -----------------------
# 创建机械臂对象：参数为串口号（根据硬件/板子选择）。
#   示例：rb.Robot(3) 表示使用串口 3；若使用不同板子可切换为 rb.Robot(1) 等。
robot = rb.Robot(3)
# 可选配置：手动设置复位步数/角度（若需要，请取消注释并根据实际值调整）
# robot.Set_Endstep(900,1800,3780,0)

# 创建 SPI LCD 显示对象，用于将摄像头图像显示到屏幕
lcd = display.SPIDisplay()

# 将机械臂回到初始位置（复位）。注意：若机械臂出现异常，可能需要重启机械臂硬件。
robot.home_setting()


def parse_move_line(line):
    """解析一行运动指令字符串并返回包含数值的字典。

    支持的指令键：X, Y, Z, E, F, S
    - X, Y, Z: 空间位置（浮点数）
    - E, F: 预留/自定义参数（浮点数）
    - S: 舵机角度（用于夹爪，通常为整数）

    示例行："X0 Y120 Z220 E0 F0 S45"

    返回格式：{'X': float or None, 'Y': ..., 'Z': ..., 'E': ..., 'F': ..., 'S': ...}
    未在行中指定的键其值为 None。
    """
    parts = line.split()
    cmd = {'X': None, 'Y': None, 'Z': None, 'E': None, 'F': None, 'S': None}
    for p in parts:
        if len(p) < 2:
            continue
        key = p[0].upper()
        try:
            val = float(p[1:])
        except Exception:
            # 如果无法解析数值，则忽略该段
            continue
        if key in cmd:
            cmd[key] = val
    return cmd


def execute_moves_from_file(robot, filename="move.txt", delay_between=1.0):
    """从文本文件按行读取移动指令并发送给机械臂。

    - `robot`: Robot_arm 的实例，用于发送运动命令
    - `filename`: 指令文件路径，默认在当前目录下为 `move.txt`
    - `delay_between`: 在执行两个 XYZ 移动之间的延迟（秒），用于给机械结构留出时间

    文件格式要求：每行一条指令，可包含注释行（以 `#` 开头）和空行。
    每行可以只包含部分参数（例如只设置舵机 S），函数会根据存在的字段执行相应动作。
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print('无法打开指令文件:', filename, e)
        return

    for i, line in enumerate(lines):
        line = line.strip()
        # 跳过空行或注释行
        if not line or line.startswith('#'):
            continue
        cmd = parse_move_line(line)
        print('执行指令行', i+1, cmd)
        try:
            # 如果同时提供了 X、Y、Z，则进行空间移动
            if cmd['X'] is not None and cmd['Y'] is not None and cmd['Z'] is not None:
                E = cmd['E'] if cmd['E'] is not None else 0
                F = cmd['F'] if cmd['F'] is not None else 0
                robot.set_xyz_point(cmd['X'], cmd['Y'], cmd['Z'], E, F)
                # 等待一段时间，给电机完成动作（可替换为状态查询/回执检查）
                time.sleep(delay_between)

            # 如果提供了 S 字段，则设定舵机角度（通常为夹爪）
            if cmd['S'] is not None:
                robot.Servo(int(cmd['S']))
                # Servo 命令通常会有串口返回，稍作停顿以稳定
                time.sleep(0.2)
        except Exception as e:
            print('执行指令时出错:', e)
            # 继续执行下一行，不让单行错误中断整个序列
            continue


# 启动时从文件执行一次指令（如果需要可改成按键触发或循环调用）
execute_moves_from_file(robot, "move.txt", delay_between=1.0)


# ----------------------- 主循环：采集图像并显示 -----------------------
while True:
    # 捕获一帧图像
    img = sensor.snapshot()

    # 读取 AD 按键输入，用于通过按键控制机械臂（Robot_arm 中实现）
    key = robot.ad_key_control()
    if key != 0:
        # 若按键返回非零值，打印以便调试
        print(key)

    # 在图像上绘制提示文字，并将图像按 90 度旋转后写入 LCD
    img.draw_string(0, 0, "Hello Robot!", color=(255, 0, 0))
    lcd.write(img.copy(hint=image.ROTATE_90))

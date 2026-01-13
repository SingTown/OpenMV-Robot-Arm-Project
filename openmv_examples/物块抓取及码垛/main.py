# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com


"""
物块抓取及码垛主程序（带注释）

功能概述：
- 使用摄像头与神经网络（FOMO/TFLite 模型）检测物块颜色/类别
- 根据检测结果控制机械臂抓取并将物块放置到指定堆叠区域

本文件适用于 OpenMV 或兼容环境，依赖模块：`sensor`, `image`, `ml`, `Robot_arm` 等。
"""

import sensor, image, time, ml, math, uos, gc
import Robot_arm as rb
import machine


# ---------------- 摄像头与硬件初始化 ----------------
sensor.reset()                         # 重置并初始化摄像头
sensor.set_pixformat(sensor.RGB565)    # 使用彩色 (RGB565)，需要时可改为 GRAYSCALE
sensor.set_framesize(sensor.QVGA)      # QVGA 分辨率 (320x240)
sensor.skip_frames(time=2000)          # 等待摄像头稳定

# 创建机械臂对象，参数为串口号（根据硬件板子选择）
robot = rb.Robot(3)  # 常见 H7 系列使用串口 3
# robot = rb.Robot(1)  # 若为其他板子/串口，取消注释并修改

# 机械臂复位到初始安全位置
robot.home_setting()
robot.Servo(0)                          # 舵机复位（通常为张开/关闭的中立位置）
robot.set_xyz_point(0, 174, 290, 0, 0)  # 将机械臂移动到一个观察/等待的初始点
time.sleep_ms(1000)


# ---------------- 全局参数（可按需调整） ----------------
min_confidence = 0.5  # 神经网络置信度阈值

# 加载神经网络模型（trained.tflite），并尽量将模型加载到 framebuffer
# 这里通过比较文件大小与可用内存做简单判断
net = ml.Model("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
print(net)

# 标签文件，第一行为背景（background），后续为识别类别（如 blue, yellow）
labels = [line.rstrip('\n') for line in open("labels.txt")]
print(labels)

# 绘制检测框时使用的颜色表，按类别索引对应
colors = [
    (255, 0, 0),    # 红
    (0, 255, 0),    # 绿
    (255, 255, 0),  # 黄
    (0, 0, 255),    # 蓝
    (255, 0, 255),  # 紫
    (0, 255, 255),  # 青
    (255, 255, 255) # 白
]

# 二值化阈值（用于中间的 blob 检测），基于置信度阈值转换到 0-255
threshold_list = [(math.ceil(min_confidence * 255), 255)]


def fomo_post_process(model, inputs, outputs):
    """FOMO 模型的输出后处理，将模型输出转换为每类的检测框列表。

    返回值为列表，每个元素为该类别的检测框列表，检测框为 (x, y, w, h, score)。
    - model: 已加载的 ml.Model 实例
    - inputs: 模型输入信息（包含 roi 等）
    - outputs: 原始模型输出张量
    """
    ob, oh, ow, oc = model.output_shape[0]

    # 将模型输出坐标映射回原始图像坐标
    x_scale = inputs[0].roi[2] / ow
    y_scale = inputs[0].roi[3] / oh
    scale = min(x_scale, y_scale)
    x_offset = ((inputs[0].roi[2] - (ow * scale)) / 2) + inputs[0].roi[0]
    y_offset = ((inputs[0].roi[3] - (ow * scale)) / 2) + inputs[0].roi[1]

    l = [[] for _ in range(oc)]  # 每个类别对应一个列表

    # 遍历每个类别的热力图，使用 find_blobs 进一步提取连通区域
    for i in range(oc):
        img = image.Image(outputs[0][0, :, :, i] * 255)
        blobs = img.find_blobs(
            threshold_list, x_stride=1, y_stride=1, area_threshold=1, pixels_threshold=1
        )
        for b in blobs:
            rect = b.rect()
            x, y, w, h = rect
            # 使用区域平均亮度作为置信度近似（归一化到 0-1）
            score = img.get_statistics(thresholds=threshold_list, roi=rect).l_mean() / 255.0
            # 映射回原图坐标并按比例缩放宽高
            x = int((x * scale) + x_offset)
            y = int((y * scale) + y_offset)
            w = int(w * scale)
            h = int(h * scale)
            l[i].append((x, y, w, h, score))
    return l


# ---------------- 机械臂堆叠区域与动作参数 ----------------
Actuator = 50  # 吸盘/夹爪动作参数偏移

# 蓝色堆叠区 (x, y) 与计数
atxb = -84
atyb = 228
b_num = 0

# 黄色堆叠区 (x, y) 与计数
atxy = -95
atyy = 168
y_num = 0

atz = 18  # 堆叠起始 Z 高度基准

# ROI：感兴趣区域，用于基于颜色的 blob 查找
ROI = (160, 120, 120, 120)

# 连续检测阈值相关（用于防抖判定）
a = 0

# LAB 颜色阈值示例（YELLOW / BLUE），用于基于颜色的 blob 检测
YELLOW = [(45, 100, -128, 2, 16, 127)]
BLUE = [(0, 41, -128, 127, -128, 127)]


def Robot_move_ai(flag, a):
    """基于神经网络检测结果的抓取与堆叠动作。

    - flag: 检测到的类别标签（如 'blue' 或 'yellow'）
    - a: 连续检测到目标的帧数（用于防抖）

    该函数在检测稳定（a >= 20）时执行抓取、移动、堆叠并更新计数器。
    """
    global b_num, y_num

    # 注意：这里的字符串匹配与大小写/换行有关（原代码曾出现 "blue\r"）
    if flag == "blue\r" and a >= 20:
        # 等待并准备抓取
        time.sleep_ms(1000)
        a = 0
        flag = 0
        robot.Servo(0)
        robot.set_xyz_point(35, 194, atz + Actuator, 0, 0)  # 抓取高度
        time.sleep_ms(1000)
        robot.Servo(60)  # 吸取/夹取
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,150 + b_num * 25,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(-50,210,150 + b_num * 25,0,0)
        time.sleep_ms(1000)
        # 移动到蓝色堆叠区并放置，堆叠高度随计数增加
        robot.set_xyz_point(atxb, atyb, 25 + Actuator + b_num * 25, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(0)  # 放下
        time.sleep_ms(1000)
        robot.set_xyz_point(0, 174, 240 + Actuator, 0, 0)  # 返回观察点
        time.sleep_ms(1000)
        b_num += 1

    if flag == "yellow" and a >= 20:
        time.sleep_ms(1000)
        a = 0
        flag = 0
        robot.Servo(0)
        robot.set_xyz_point(35, 194, atz + Actuator, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,200 + y_num * 25,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy, atyy, 25 + Actuator + y_num * 25, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0, 174, 240 + Actuator, 0, 0)
        time.sleep_ms(1000)
        y_num += 1


def Robot_move_blobs(flag, a):
    """基于颜色二值化 blob 检测的抓取与堆叠动作。

    与 `Robot_move_ai` 类似，但用于基于 `find_blobs` 的检测分支。
    """
    global b_num, y_num

    if flag == 'BLUE' and a >= 0:
        time.sleep_ms(1000)
        robot.Servo(0)
        robot.set_xyz_point(35, 194, atz + Actuator, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,150 + b_num * 25,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(-50,210,150 + b_num * 25,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb, atyb, 25 + Actuator + b_num * 25, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0, 174, 240 + Actuator, 0, 0)
        time.sleep_ms(1000)
        b_num += 1

    if flag == 'YELLOW' and a >= 0:
        time.sleep_ms(1000)
        robot.Servo(0)
        robot.set_xyz_point(35, 194, atz + Actuator, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,140 + y_num * 25,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy, atyy, 25 + Actuator + y_num * 25, 0, 0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0, 174, 240 + Actuator, 0, 0)
        time.sleep_ms(1000)
        y_num += 1


def main_ai():
    """主循环（基于神经网络检测）：

    - 连续读取图像并通过模型预测
    - 在检测到目标并稳定（连续帧数达到阈值）后触发 `Robot_move_ai`
    """
    while True:
        a = 0
        flag = 0
        while True:
            img = sensor.snapshot()
            # 使用模型预测；fomo_post_process 会将输出转换为每类检测框列表
            for i, detection_list in enumerate(net.predict([img], callback=fomo_post_process)):
                if i == 0:
                    continue  # 跳过 background 类
                for x, y, w, h, score in detection_list:
                    center_x = math.floor(x + (w / 2))
                    center_y = math.floor(y + (h / 2))
                    # 仅在置信度与位置满足条件时认为是有效目标（右侧区域筛选）
                    if score > min_confidence and center_x > 120:
                        flag = labels[i]
                        a += 1
                        img.draw_circle((center_x, center_y, 12), color=colors[i])
            if flag != 0 and a >= 20:
                print(flag, a)
                break
        Robot_move_ai(flag, a)


def main_blobs():
    """主循环（基于颜色阈值的 blob 检测）：

    - 使用 `find_blobs` 在 ROI 内查找指定颜色范围
    - 通过连续检测计数实现防抖，达到阈值后触发抓取动作
    """
    while True:
        a = 0
        flag = 0
        last_flag = 0
        while True:
            img = sensor.snapshot()
            detected = 0
            # 黄色物块检测
            for blob in img.find_blobs([YELLOW[0]], pixels_threshold=200, area_threshold=200, merge=True, roi=ROI):
                if blob:
                    img.draw_rectangle(blob.rect())
                    img.draw_cross(blob.cx(), blob.cy())
                    flag = 'YELLOW'
                    detected = 1
                    break
            # 蓝色物块检测（若未检测到黄色）
            if not detected:
                for blob in img.find_blobs([BLUE[0]], pixels_threshold=200, area_threshold=200, merge=True, roi=ROI):
                    if blob:
                        img.draw_rectangle(blob.rect())
                        img.draw_cross(blob.cx(), blob.cy())
                        flag = 'BLUE'
                        detected = 1
                        break
            # 连续识别逻辑：只有连续多帧相同类别才认为有效
            if detected:
                if last_flag == flag:
                    a += 1
                else:
                    a = 1
                last_flag = flag
            else:
                a = 0
                flag = 0
                last_flag = 0
            # 达到阈值则触发移动
            if flag != 0 and a >= 40:
                print(flag, a)
                break
        Robot_move_blobs(flag, a)
        a = 0


# ---------------- 运行入口与模式选择 ----------------
flag = 0


def choice_event():
    """通过 AD 按键选择运行模式：
    - key == 10: 运行基于神经网络的 `main_ai`
    - key == 11: 运行基于 blob 的 `main_blobs`
    - 其他按键或超时按键会返回并重启或退出
    """
    global flag
    while True:
        key = robot.ad_key_control()
        if key == 10:
            print("10")
            flag = 1
            break
        elif key == 11:
            print("11")
            flag = 2
            break
        elif key == 12:
            print("12")
            flag = key
            break
        elif key != 0 and key is not None:
            print(key)
            flag = key
            break
    return flag


# 等待用户通过按键选择任务模式
choice_event()

if flag == 1:
    main_ai()
elif flag == 2:
    main_blobs()
else:
    # 未选择有效模式则重启设备以回到安全状态
    machine.reset()

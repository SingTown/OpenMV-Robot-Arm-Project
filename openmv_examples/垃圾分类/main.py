# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

"""
垃圾分类主程序

说明：
- 本脚本负责从摄像头采集图像，使用已部署的 TFLite 模型进行分类，
  并将识别结果传给机械臂执行分拣操作。
- 请确保同目录下存在 `model.tflite` 与 `labels.txt`，以及 `Robot_arm.py` 和 `move.py`。
"""

# 导入核心库：图像传感器、机器学习模型、机械臂控制以及动作模块
import sensor, ml
import Robot_arm as rb
import move

# ---------- 传感器（摄像头）初始化 ----------
sensor.reset()                          # 重置摄像头
sensor.set_pixformat(sensor.RGB565)     # 设置像素格式为 RGB565（彩色）
sensor.set_framesize(sensor.QVGA)       # 设置分辨率为 QVGA (320x240)
sensor.skip_frames(time=2000)           # 跳过若干帧，等候相机稳定


# ---------- 机械臂初始化 ----------
# 创建机械臂对象：参数为串口号（根据硬件不同选择 1 或 3）
robot = rb.Robot(3)  # 使用串口3（例如 H7 板子）
# 若需用串口1，请取消下一行注释并调整为 robot = rb.Robot(1)
# robot = rb.Robot(1)
robot.home_setting()  # 机械臂回到初始位（复位）


# ---------- 可调参数 ----------
Actuator = 75   # 夹持器/执行器动作力度或位置（根据具体实现含义）

# 识别区域位移（相对于屏幕中心的偏移）
ShiftX = 40
ShiftY = 0

# 模型输入尺寸（宽、高）——与训练时一致
w = 128
h = 128

# 计算感兴趣区域（ROI）：在 320x240 图像上的中心区域并加上偏移
roi = (int((320 - w) / 2) + ShiftX, int((240 - h) / 2) + ShiftY, w, h)


# ---------- 标签与模型加载 ----------
with open('labels.txt', 'r') as file:
    # 读取标签文件，去除空行和换行符，得到标签列表
    labels = [line.strip() for line in file if line.strip()]
    print('Loaded labels:', labels)

# 加载 TFLite 模型到 framebuffer（或内存），名称必须与工程中一致
model = ml.Model("model.tflite", load_to_fb=True)
print('Model loaded:', model)

# 归一化器：将图像像素缩放到模型期望范围
norm = ml.Normalization(scale=(0.0, 1.0))


def garbage():
    """
    垃圾分类识别函数

    算法流程：
    - 连续采集若干帧（当前为10帧），对每帧进行裁剪并归一化
    - 将图像输入模型，得到各类置信度 scores
    - 对每帧选择置信度最高的标签，若最高置信度 > 0.8 则计入投票
    - 最终对投票结果采用众数（出现次数最多的标签）作为返回结果

    返回：
    - 字符串：识别出的垃圾类别（来自 `labels.txt`）
    - None：若无一帧达到置信度阈值（0.8）或未能识别
    """
    results = []  # 存放多次检测通过阈值的标签

    # 连续采样多帧以提高鲁棒性
    for _ in range(10):
        img = sensor.snapshot()  # 捕获当前帧

        # 在显示上绘制识别区域，便于调试观察
        img.draw_rectangle(int((320 - w) / 2) + ShiftX, int((240 - h) / 2) + ShiftY, w, h, color=(0, 0, 255))

        # 裁剪出模型输入区域并进行归一化（与训练时预处理一致）
        img2 = img.copy(roi=roi)
        input_data = [norm(img2)]

        # 模型推理，返回每个类别的置信度列表
        scores = model.predict(input_data)[0].flatten().tolist()

        # 找到该帧中置信度最高的标签及其分数
        max_score = 0
        max_label = None
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label

        # 仅当最高置信度超过阈值时，才把结果计入投票
        if max_score > 0.8:
            results.append(max_label)

    # 若多帧检测均未达到阈值，返回 None
    if not results:
        return None

    # 统计众数（出现次数最多的标签）并返回
    count_dict = {}
    for label in results:
        count_dict[label] = count_dict.get(label, 0) + 1

    max_count = 0
    best_label = None
    for label, count in count_dict.items():
        if count > max_count:
            max_count = count
            best_label = label

    return best_label



# ---------- 主循环：持续识别并驱动机械臂分拣 ----------
while True:
    labelb = garbage()          # 调用识别函数
    print('识别结果:', labelb)  # 打印识别结果，便于串口调试查看

    if labelb is not None:
        # 若识别成功，则调用 move 模块执行具体分拣动作
        # 参数含义：robot 对象、夹取执行器位置/力度、识别出的标签
        move.execute_garbage_sorting(robot, Actuator, labelb)
    else:
        # 未识别到可信结果，输出提示（也可以在此处添加等待或重试逻辑）
        print("未识别到垃圾或识别置信度过低")

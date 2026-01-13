# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com


"""三子棋演示主程序
负责摄像头图像获取、模型识别、棋盘状态管理和机械臂落子控制。
此文件运行在 OpenMV/MicroPython 环境，上层依赖：`Robot_arm`, `move`, `chess`, `display` 等模块。
"""

import sensor, ml
import Robot_arm as rb
import chess
import move
import display
import machine
import image


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口(H7)。
#robot = rb.Robot(1) #初始化，设置串口1为机械臂通讯串口(RT)。
robot.home_setting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行
lcd = display.SPIDisplay()    # 创建SPI显示屏对象

Actuator = 75

# 九宫格参数配置
distance = 50   # 九宫格中每个方格的间距（像素）
block = 32      # 每个检测区域的边长（像素）
ShiftX = 33     # 九宫格整体在X轴上的偏移量（像素）
ShiftY = -1     # 九宫格整体在Y轴上的偏移量（像素）

##棋子位置测试程序
# import time
# move.get_piece_black(robot,Actuator,4)
# for i in range(5):
#     move.get_piece_black(robot,Actuator,i)
#     robot.relay(False)
#     time.sleep_ms(1000)

# move.get_piece_white(robot,Actuator,4)
# for i in range(5):
#     move.get_piece_white(robot,Actuator,i)
#     robot.relay(False)
#     time.sleep_ms(1000)

# 生成九宫格的区域位置
def generate_centered_rois(width, height, b, k):
    """生成居中的 3x3 棋盘检测区域（ROI）列表。

    参数:
    - width, height: 图像宽高
    - b: 每个大格子的间距（用于计算 3x3 矩阵的总尺寸）
    - k: 每个检测区域的边长

    返回:
    - 一个 3x3 的 list，元素为 `(x, y, w, h)` 的 ROI 元组，适用于 `img.copy(roi=...)`。
    """
    rois = []
    # 计算整个3x3矩阵的宽度和高度（像素）
    total_width = 3 * b
    total_height = 3 * b

    # 计算左上角的起始点，使矩阵居中，并加上偏移量
    start_x = (width - total_width) // 2 + ShiftX
    start_y = (height - total_height) // 2 + ShiftY

    for i in range(3):
        row = []
        for j in range(3):
            x_center = start_x + j * b + b // 2
            y_center = start_y + i * b + b // 2
            x = x_center - k // 2
            y = y_center - k // 2
            # 每个 ROI 使用左上角坐标和宽高表示
            row.append((x, y, k, k))
        rois.append(row)

    return rois

# 九宫格的区域位置
rois = generate_centered_rois(sensor.width(), sensor.height(), distance, block)

# 棋盘数组
# 黑子：X
# 白子：O
# 没有棋子：空字符串
board = [
     [" "," "," "],
     [" "," "," "],
     [" "," "," "],
]

with open('labels.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]
    print(labels)
model = ml.Model("model.tflite", load_to_fb=True)
print(model)
norm = ml.Normalization(scale = (0.0,1.0))

def Net(img2):
    """对单个 ROI 图像进行模型预测并返回最终标签。

    使用多次预测并取多数表决的方式以提高鲁棒性：
    - 对传入的 `img2` 进行 `norm` 预处理，然后多次调用模型预测
    - 只统计置信度 >= 0.8 的预测结果
    - 返回出现次数最多的标签（众数），若无高置信度预测则返回 `None`
    """
    results = []  # 存储多次识别得到的高置信标签
    # 循环多次做推理以降低单次误判影响
    for _ in range(30):
        input = [norm(img2)]  # 将像素值归一化到 0.0~1.0
        scores = model.predict(input)[0].flatten().tolist()

        # 找到当前推理的最高分标签及其置信度
        max_score = 0
        max_label = None
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label

        # 仅记录置信度较高的结果以减少噪声影响
        if max_score > 0.8:
            results.append(max_label)

    # 如果没有有效结果则返回 None
    if not results:
        return None

    # 统计众数并返回出现次数最多的标签
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

def get_color(img):
    """扫描当前帧的 3x3 ROI，并更新全局 `board` 棋盘状态。

    注意：本函数依赖调用处已有 `img = sensor.snapshot()`，并使用 `img.copy(roi=...)`。
    如果在其它上下文调用，需要保证 `img` 已经被定义为当前帧。
    """
    # 遍历所有 ROI，调用模型识别并写回全局 board
    for y in range(len(rois)):
        for x in range(len(rois[y])):
            img2 = img.copy(roi=rois[y][x])
            label = Net(img2)
            print(label)
            if label == "black":
                board[y][x] = "black"
            elif label == "white":
                board[y][x] = "white"
            else:
                # 识别不到或为背景则设置为 None
                board[y][x] = None

flag = 0
def choice_event():
    global flag
    while 1:
        key = robot.ad_key_control()
        # print(b)
        if key == 10:
            print("10")
            flag = key
            break
        elif key == 11:
            print("11")
            flag = key
            break
        elif key == 12:
            print("12")
            flag = key
            break
        elif key !=0 and key != None :
            print(key)
            flag = key
            break
    return flag

"""监听按键选择事件并返回对应事件标志。

该函数持续查询 `robot.ad_key_control()`，当接收到非 0 且非 None 的键值时，
将其赋值给全局 `flag` 并返回。常用的按键值映射在上层代码中使用（如 1/2/3）。
"""


def put_piece(color,n):
    x = 1
    y = 1
    print(x,y)
    if color == 'black':
        move.get_piece_black(robot,Actuator,n)
    elif color == 'white':
        move.get_piece_white(robot,Actuator,n)
    move.move2pan(robot,Actuator,x,y)


def img_show(player):
    """在屏幕上显示当前状态信息。

    参数 `player` 用于显示当前玩家或等待状态的字符串。
    """
    img = sensor.snapshot()
    # 在图像上绘制提示信息，随后通过 SPI LCD 显示（旋转90度以适配屏幕）
    img.draw_string(0,120,"DEMO",scale = 1  ,color=(255,0,0))  # 在图像上显示欢迎语
    img.draw_string(0,140,f"event:{int(flag)}",color=(255,0,0))
    img.draw_string(0,160,"USER:"+player,color=(255,0,0))
    lcd.write(img.copy(hint=image.ROTATE_90))


def event_1():
    """事件1：由黑方先手。

    控制流程：
    - 机械臂先放置黑子（调用 `put_piece`）
    - 进入循环：获取帧、识别棋盘、在图像上绘制检测结果并判断胜负
    - 当轮到 AI（示例中为 black）时，调用 `chess.best_move` 获取落子并控制机械臂执行
    - 等待按键继续下一步/下一帧
    """
    put_piece('black',0)
    n=1
    while True:
        img = sensor.snapshot()
        global board
        # 识别棋盘并打印当前状态
        get_color(img)
        for line in board:
            print(line)

        # 在图像上绘制每个格子的检测颜色（红: black, 蓝: white, 绿: 空）
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None or board[y][x] == "background" :
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        # 若有胜者则显示并等待重置
        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                img.draw_string(0,180,"WINNER:"+chess.check_winner(board),color=(255,0,0))
                lcd.write(img.copy(hint=image.ROTATE_90))
                if key !=0 and key != None :
                    machine.reset()
                    break

        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是 AI 执子，则计算最佳落子并驱动机械臂
        if player == "black":
            move_pos = chess.best_move(board, player)
            print("AI选择位置:", move_pos)
            if move_pos is not None:
                y, x = move_pos
                board[y][x] = player
                move.get_piece_black(robot,Actuator,n)
                move.move2pan(robot,Actuator,y,x)
                n = n + 1
        else:
            # 等待人类输入落子（通过按键或其它输入）
            pass

        # 等待按键确认继续下一步
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break


def event_2():
    """事件2：由白方先手或白方为 AI 的流程。

    与 `event_1` 类似，但 AI 执子判断为 white，且初始显示略有差别。
    """
    n = 0
    img_show('black')
    while True:
        img = sensor.snapshot()
        global board
        # 识别棋盘并打印当前状态
        get_color(img)
        for line in board:
            print(line)

        # 绘制检测区域颜色
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None:
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        # 胜利处理
        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                img.draw_string(0,180,"WINNER:"+chess.check_winner(board),color=(255,0,0))
                lcd.write(img.copy(hint=image.ROTATE_90))
                if key !=0 and key != None :
                    machine.reset()
                    break

        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是 AI 执子（示例中为 white），则计算最佳落子并驱动机械臂
        if player == "white":
            move_pos = chess.best_move(board, player)
            print("AI选择位置:", move_pos)
            if move_pos is not None:
                y, x = move_pos
                board[y][x] = player
                move.get_piece_white(robot,Actuator,n)
                move.move2pan(robot,Actuator,y,x)
                n = n + 1
        else:
            # 等待人类输入落子
            pass

        # 等待按键确认继续下一步
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break


img_show('WAITING')

#等待任务选择
choice_event()

if flag == 1:
    print("event 1")
    img_show('WHITE')
    event_1()

elif flag == 2:
    print("event 2")
    img_show('BLACK')
    event_2()

elif flag == 3:
    color = (0,255,0)
    while True:
        img = sensor.snapshot()
        get_color(img)
        for line in board:
            print(line)
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None:
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)
else:
    machine.reset()

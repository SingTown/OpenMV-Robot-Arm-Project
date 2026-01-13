# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

# --------------------------------------------------
# 说明：这是主程序入口，用于在 OpenMV 上运行
# 包含：传感器初始化、模型加载、棋盘识别、机械臂控制事件
# 注释以中文为主，目的是帮助理解程序流程与关键变量
# --------------------------------------------------

import sensor, ml
import Robot_arm as rb
import chess
import move
import display
import machine
import image


sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 设置像素格式为 RGB565
sensor.set_framesize(sensor.QVGA)    # 设置分辨率为 QVGA（320x240）
sensor.skip_frames(time = 2000)      # 等待传感器稳定

Actuator = 75  # 机械爪执行器的开合力度/通道（根据具体固件设定）

robot = rb.Robot(3)  # 初始化机械臂，使用串口3（H7）与机械臂通讯
# 如果你的板子使用串口1，请改为： robot = rb.Robot(1)
robot.home_setting()   # 机械臂回零复位（若异常请重启机械臂并重试）
lcd = display.SPIDisplay()    # 创建 SPI 屏幕显示对象

# 九宫格相关参数：
# distance: 格子之间中心到中心的距离（像素）
# block: 每个格子的边长（像素），用于计算 ROI
# ShiftX/ShiftY: 在图像中心基础上的微调偏移，用于对齐棋盘
distance = 50
block = 32
ShiftX = 33
ShiftY = 1


def img_show(player):
    # 捕获一帧图像并在屏幕上显示当前状态（简要信息）
    img = sensor.snapshot()
    img.draw_string(0,120,"DEMO",scale = 1  ,color=(255,0,0))  # 在图像上显示欢迎语
    img.draw_string(0,140,f"EVENT:{int(flag)}",color=(255,0,0))  # 显示当前事件编号
    img.draw_string(0,160,"USER:"+player,color=(255,0,0))       # 显示当前玩家/模式
    lcd.write(img.copy(hint=image.ROTATE_90))  # 将图像旋转并写入 SPI 显示屏

# --------- 工具函数：深拷贝棋盘 ---------
def deepcopy_board(src):
    # 返回棋盘的深拷贝，避免引用导致原棋盘被意外修改
    return [[cell for cell in row] for row in src]


# 生成九宫格的区域位置
def generate_centered_rois(width, height, b, k):
    # 生成 3x3 九宫格的 ROI（感兴趣区域）
    # 参数说明：width/height 为图像尺寸，b 为格子间距（distance），k 为格子大小（block）
    rois = []
    # 计算整个 3x3 矩阵的宽高（以像素计）
    total_width = 3 * b
    total_height = 3 * b

    # 计算左上角起点，目的是让九宫格居中，再加上微调偏移量 ShiftX/ShiftY
    start_x = (width - total_width) // 2 + ShiftX
    start_y = (height - total_height) // 2 + ShiftY

    # 对每个格子计算其 ROI（x, y, w, h）并返回一个 3x3 的列表
    for i in range(3):
        row = []
        for j in range(3):
            x_center = start_x + j * b + b // 2
            y_center = start_y + i * b + b // 2
            x = x_center - k // 2
            y = y_center - k // 2
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
    # 使用已加载的 TFLite 模型对单个 ROI 图像进行预测
    # 为了提高鲁棒性，重复多次预测并取众数作为最终标签
    results = []  # 存储每次识别的高置信度结果
    # 重复多次识别以减少单次误判（这里循环 30 次，可根据速度调整）
    for _ in range(30):
        input = [norm(img2)]  # 归一化输入：0~255 -> 0.0~1.0
        scores = model.predict(input)[0].flatten().tolist()
        # 找到最高分标签
        max_score = 0
        max_label = None
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label

        # 仅记录置信度高（>0.8）的结果
        if max_score > 0.8:
            results.append(max_label)

    # 若没有高置信度结果，返回 None
    if not results:
        return None

    # 统计众数（出现次数最多的标签）并作为最终输出
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
    # 图像识别得到棋盘数组
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
                # 未识别到棋子或为背景时，设置为 None
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


def put_piece(color,n):
    x = 1
    y = 1
    while True:
        key = choice_event()
        if key !=0 and key != None :
            if key == 1:
                x = 0
                y = 0
            elif key == 2:
                x = 0
                y = 1
            elif key == 3:
                x = 0
                y = 2
            elif key == 4:
                x = 1
                y = 0
            elif key == 5:
                x = 1
                y = 1
            elif key == 6:
                x = 1
                y = 2
            elif key == 7:
                x = 2
                y = 0
            elif key == 8:
                x = 2
                y = 1
            elif key == 9:
                x = 2
                y = 2
            break
    # 打印目标格子坐标并控制机械臂取放对应颜色的棋子
    print(x,y)
    if color == 'black':
        move.get_piece_black(robot,Actuator,n)
    elif color == 'white':
        move.get_piece_white(robot,Actuator,n)
    move.move2pan(robot,Actuator,x,y)


def put_piece_45(color,n):
    x = 1
    y = 1
    while True:
        key = choice_event()
        if key !=0 and key != None :
            if key == 1:
                x = 0
                y = 0
            elif key == 2:
                x = 0
                y = 1
            elif key == 3:
                x = 0
                y = 2
            elif key == 4:
                x = 1
                y = 0
            elif key == 5:
                x = 1
                y = 1
            elif key == 6:
                x = 1
                y = 2
            elif key == 7:
                x = 2
                y = 0
            elif key == 8:
                x = 2
                y = 1
            elif key == 9:
                x = 2
                y = 2
            break
    # 与 put_piece 类似，但使用 45 度放置函数（适用于不同摆放角度）
    print(x,y)
    if color == 'black':
        move.get_piece_black(robot,Actuator,n)
    elif color == 'white':
        move.get_piece_white(robot,Actuator,n)
    move.move2pan_45(robot,Actuator,x,y)


def event_1():
    # 事件1：示例演示，获取一颗黑子并放到中心，然后重启
    move.get_piece_black(robot,Actuator,4)
    move.move2pan(robot,Actuator,1,1)
    machine.reset()

def event_2():
    # 事件2：按序放置黑白棋子（示例序列），结束后重启
    put_piece('black',0)
    put_piece('black',1)
    put_piece('white',0)
    put_piece('white',1)
    machine.reset()


def event_3():
    # 事件3：使用 45 度摆放的演示序列
    put_piece_45('black',0)
    put_piece_45('black',1)
    put_piece_45('white',0)
    put_piece_45('white',1)
    machine.reset()

def event_4():
    # 事件4：人机对弈示例，黑方先行（机械臂放一颗黑子开始）
    put_piece('black',0)
    n=1
    while True:
        img = sensor.snapshot()
        global board
        # 识别棋盘
        get_color(img)
        for line in board:
            print(line)
        # 画棋盘数组
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None or board[y][x] == "background" :
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        # print("当前胜利者为：",chess.check_winner(board))
        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                if key !=0 and key != None :
                    machine.reset()
                    break
        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是AI执子（如white），则AI落子
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
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break

def event_5():
    # 事件5：另一路人机对弈，白方由 AI 下子示例
    n = 0
    while True:
        img = sensor.snapshot()
        global board
        # 识别棋盘
        get_color(img)
        for line in board:
            print(line)
        # 画棋盘数组
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None:
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                if key !=0 and key != None :
                    machine.reset()
                    break
        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是AI执子（如white），则AI落子
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
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break


def event_6():
    global board
    # 事件6：检测棋子被人为挪动（作弊检测），如发现则把棋子放回原位
    put_piece('black',0)
    n=1
    prev_board = deepcopy_board(board)
    while True:
        img = sensor.snapshot()
        # 识别棋盘
        get_color(img)
        # 检查棋子是否被挪动作弊
        moved = False
        for y in range(3):
            for x in range(3):
                # 如果原来有棋子，现在没了，说明被挪走
                if prev_board[y][x] in ("black", "white") and board[y][x] != prev_board[y][x]:
                    # 查找该棋子被挪动到哪里
                    found = False
                    for ny in range(3):
                        for nx in range(3):
                            if (ny != y or nx != x) and board[ny][nx] == prev_board[y][x] and prev_board[ny][nx] != prev_board[y][x]:
                                print("棋子从(%d,%d)被挪动到(%d,%d)" % (y, x, ny, nx))
                                print("检测到棋子被挪动，放回原位","从",ny,nx, "到", y, x)
                                found = True
                                # 机械臂放回棋子
                                move.get_pan_piece(robot,Actuator,ny,nx)
                                move.move2pan(robot,Actuator,y, x)
                    if not found:
                        print("棋子从(%d,%d)被挪动，未检测到新位置" % (y, x))
                    board[y][x] = prev_board[y][x]
                    moved = True
        if moved:
            # 放回后，重新识别棋盘
            get_color(img)
        prev_board = deepcopy_board(board)
        for line in board:
            print(line)
        # 画棋盘数组
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None or board[y][x] == "background" :
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        # print("当前胜利者为：",chess.check_winner(board))
        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                if key !=0 and key != None :
                    machine.reset()
                    break
        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是AI执子（如white），则AI落子
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
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break

img_show('WAITING')
#等待任务选择
choice_event()

if flag == 1:
    print("event 1")
    img_show('event 1')
    event_1()

elif flag == 2:
    print("event 2")
    img_show('event 2')
    event_2()

elif flag == 3:
    print("event 3_45")
    img_show('event 3')
    event_3()

elif flag == 4:
    print("event 4")
    img_show('WHITE')
    event_4()

elif flag == 5:
    print("event 5")
    img_show('BLACK')
    event_5()


elif flag == 6:
    print("event 6")
    img_show('WHITE')
    event_6()

elif flag == 7:
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

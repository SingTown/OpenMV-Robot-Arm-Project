# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com


# 导入硬件相关库
H7 = True  # 根据实际硬件平台设置此标志, True表示H743系列

if H7:
    from pyb import UART, ADC   # 串口、舵机、ADC模块（pyb）
else:
    from machine import UART, ADC   # 串口、舵机、ADC模块（machine）

import time, re                    # 时间和正则表达式模块
import sensor                      # 摄像头模块
import machine                    # 机器相关模块

# 机械臂坐标系参数
base_h = 290 - 172 + 52            # 基准高度修正值（固定）
Actuator = 0                       # 执行器高度，默认0
ON = 1                             # 继电器开关常量

"""
机械臂只可在第一、二、三象限活动，第四象限由于Z轴限位开关阻挡无法活动，即270°旋转范围。
Y轴正方向为机械臂正前方
X轴正方向为机械臂右侧
Z轴正方向为机械臂向上
"""

# 机械臂活动范围参数
h_max = 322        # Z轴最大高度
h_min = 32         # Z轴最小高度
x_max = 280        # X轴最大坐标
x_min = -280       # X轴最小坐标
y_max = 280        # Y轴最大坐标
y_min = -280       # Y轴最小坐标
Servo_max = 76     # 舵机夹爪最大角度
Servo_min = 0      # 舵机夹爪最小角度



def parse_position(data):
    """
    解析机械臂串口返回的坐标字符串，提取X、Y、Z、E坐标。
    :param data: 形如 "INFO: CURRENT POSITION: [X:0.00 Y:174.00 Z:120.00 E:0.00]" 的字符串
    :return: 坐标字典 {'X':..., 'Y':..., 'Z':..., 'E':...} 或错误信息
    """
    try:
        # 找到方括号内的内容
        start_index = data.find('[') + 1
        end_index = data.find(']')
        # 验证字符串格式
        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError("无效的输入格式 - 缺少方括号")
        coordinates_str = data[start_index:end_index]
        # 分割键值对
        pairs = coordinates_str.split()
        # 验证元素数量
        if len(pairs) < 4:
            raise ValueError(f"无效的输入格式 - 需要4个元素，实际找到{len(pairs)}")
        # 提取每个值并修正Z轴高度
        result = {
            'X': float(pairs[0].split(':')[1]),
            'Y': float(pairs[1].split(':')[1]),
            'Z': float(pairs[2].split(':')[1]) + base_h - Actuator,
            'E': float(pairs[3].split(':')[1])
        }
        return result
    except Exception as e:
        return {'error': str(e), 'input': data}



class Robot:
    def ad_key_control(self):
        """
        通过ADC模拟按键控制机械臂动作，仅保留短按（已移除长按功能）
        """
        ad_list = []
        for _ in range(50):
            if H7:
                ad_list.append((self.adc.read() * 3.3) / 4095)
            else:
                ad_list.append((self.adc.read_u16() * 3.3) / 65535)
            time.sleep_ms(1)
        ad_list.sort()
        filtered = ad_list[1:-1]
        mid_idx = len(filtered) // 2
        if len(filtered) % 2 == 0:
            ad = round((filtered[mid_idx - 1] + filtered[mid_idx]) / 2, 2)
        else:
            ad = round(filtered[mid_idx], 2)

        a = 0
        print(ad)
        # 判断动作类型（短按）
        if 0.35 > ad > 0.15:
            a = 9
            time.sleep_ms(200)

        elif ad < 0.1:
            a = 3
            time.sleep_ms(200)

        elif 1.6 > ad > 1.4:
            a = 4
            time.sleep_ms(200)

        elif 1.3 > ad > 1:
            a = 6
            time.sleep_ms(200)

        elif 0.6 > ad > 0.4:
            a = 2
            time.sleep_ms(200)

        elif 1 > ad > 0.7:
            a = 8
            time.sleep_ms(200)

        elif 2 > ad > 1.7:
            a = 1
            time.sleep_ms(200)

        elif 2.3 > ad > 2.10:
            a = 7
            time.sleep_ms(200)

        elif 2.6 > ad > 2.45:
            a = 5
            time.sleep_ms(200)

        return a
    def __init__(self, nums):
        """
        构造函数，初始化串口、舵机、ADC及机械臂初始坐标。
        :param nums: 串口号（如3）
        """
        self.uart1 = UART(nums, 115200, timeout_char=1)  # 初始化串口                        # 初始夹爪角度
        self.adc = ADC("P6")                            # ADC初始化，必须为"P6"
        self.x = 0                                       # 初始X坐标
        self.y = 174                                     # 初始Y坐标
        self.z = 292                                     # 初始Z坐标
        self.angle = 0                                   # 初始夹爪角度

    def home_setting(self):
        """
        机械臂复位，发送G28指令，等待串口返回。
        超时未返回则直接复位坐标。
        """
        data_to_send = "G28\r\n"
        print(data_to_send, "复位......")
        self.uart1.write(data_to_send)
        start = time.ticks_ms()
        timeout = 15000  # 15秒超时
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                self.angle = 45
                self.Servo(self.angle)
                self.x = 0
                self.y = 174
                self.z = 292
                print(string_data)
                break
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                self.angle = 45
                self.Servo(self.angle)
                self.x = 0
                self.y = 174
                self.z = 292
                print("复位超时，无数据返回")
                break

    def get_xyz_point(self):
        """
        查询机械臂当前坐标，发送M114指令，解析串口返回坐标。
        :return: (X, Y, Z) 坐标元组
        """
        data_to_send = "M114\r\n"
        self.uart1.write(data_to_send)
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                # 串口可能返回多行数据，逐行处理
                for line in string_data.split('\n'):
                    line = line.strip()
                    if 'CURRENT POSITION' in line:
                        position = parse_position(line)
                        if 'error' in position:
                            print(f"坐标解析失败: {position['error']} 原始数据: {position['input']}")
                            continue
                        self.x = position['X']
                        self.y = position['Y']
                        self.z = position['Z']
                        return self.x, self.y, self.z
                        break

    def get_key_val(self):
        """
        查询机械臂限位开关状态，发送M119指令。
        """
        data_to_send = "M119\r\n"
        print(data_to_send, "查询当前限位开关......")
        self.uart1.write(data_to_send)
        while(True):
            if self.uart1.any():
                 data = self.uart1.read()
                 string_data = data.decode('utf-8').strip()
                 print(string_data)
                 break

    def set_xyz_point(self, X, Y, Z, E, F):
        """
        设置机械臂目标坐标，发送G1指令。
        :param X, Y, Z, E, F: 目标坐标与速度参数
        """
        data_to_send = "G1 X{} Y{} Z{} E{} F{}\r\n".format(X, Y, Z-base_h+Actuator, E, F)
        self.x = X
        self.y = Y
        self.z = Z
        self.uart1.write(data_to_send)
        time.sleep_ms(10)

    def relay(self, state):
        """
        控制机械臂主板继电器开关。
        :param state: ON为开，其他为关
        """
        if state == ON:
            data_to_send = "M1\r\n"
        else:
            data_to_send = "M2\r\n"
        print(data_to_send)
        self.uart1.write(data_to_send)

    def Servo(self, angle):
        """
        控制主板舵机角度，发送M280指令。
        :param angle: 舵机角度
        """
        data_to_send = "M280 P{}\r\n".format(angle)
        print(data_to_send)
        self.uart1.write(data_to_send)
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                print(string_data)
                break

    def Set_Endstep(self,X,Y,Z,E):
        data_to_send = "M281 X{} Y{} Z{} E{}\r\n".format(X, Y, Z, E)
        print(data_to_send)
        self.uart1.write(data_to_send)
        # while True:
        #     if self.uart1.any():
        #         data = self.uart1.read()
        #         string_data = data.decode('utf-8').strip()
        #         print(string_data)
        #         break

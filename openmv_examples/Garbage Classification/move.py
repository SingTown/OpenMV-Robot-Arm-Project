# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com

# move.py - 机械臂垃圾分拣动作控制模块
"""
该模块包含了不同类型垃圾的机械臂抓取和分拣动作序列
支持三种垃圾分类：有害垃圾、厨余垃圾、其他垃圾
注意：此版本使用了不同的夹爪力度参数和垃圾桶布局
"""

import time

def move_harmful_waste(robot, Actuator):
    """
    有害垃圾分拣动作序列

    参数:
        robot: 机械臂控制对象
        Actuator: 执行器高度偏移量

    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到有害垃圾桶
        5. 释放垃圾并返回初始位置
    """
    print("执行有害垃圾分拣动作...")

    # 移动到抓取准备位置（中心上方）
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 打开夹爪准备抓取
    robot.Servo(10)
    time.sleep_ms(1000)

    # 进一步下降接近垃圾
    robot.set_xyz_point(0, 217, 8+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 用较大力度夹紧夹爪抓取垃圾
    robot.Servo(70)
    time.sleep_ms(1000)

    # 抬升到安全运输高度
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 移动到有害垃圾桶上方
    robot.set_xyz_point(105, 124, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到垃圾桶内
    robot.set_xyz_point(105, 124, 100+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 松开夹爪释放垃圾
    robot.Servo(20)
    time.sleep_ms(1000)

    # 返回初始位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)


def move_kitchen_garbage(robot, Actuator):
    """
    厨余垃圾分拣动作序列

    参数:
        robot: 机械臂控制对象
        Actuator: 执行器高度偏移量

    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到厨余垃圾桶
        5. 释放垃圾并返回初始位置
    """
    print("执行厨余垃圾分拣动作...")

    # 移动到抓取准备位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 打开夹爪
    robot.Servo(10)
    time.sleep_ms(1000)

    # 进一步下降
    robot.set_xyz_point(0, 217, 8+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 用中等力度夹紧垃圾
    robot.Servo(45)
    time.sleep_ms(1000)

    # 抬升到安全高度
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 移动到厨余垃圾桶上方
    robot.set_xyz_point(105, 220, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到垃圾桶内
    robot.set_xyz_point(105, 220, 100+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 释放垃圾
    robot.Servo(20)
    time.sleep_ms(1000)

    # 返回初始位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)


def move_other_garbage(robot, Actuator):
    """
    其他垃圾分拣动作序列

    参数:
        robot: 机械臂控制对象
        Actuator: 执行器高度偏移量

    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到其他垃圾桶
        5. 释放垃圾并返回初始位置
    """
    print("执行其他垃圾分拣动作...")

    # 移动到抓取准备位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 打开夹爪
    robot.Servo(10)
    time.sleep_ms(1000)

    # 进一步下降
    robot.set_xyz_point(0, 217, 5+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 用标准力度夹紧垃圾
    robot.Servo(60)
    time.sleep_ms(1000)

    # 抬升到安全高度
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 移动到其他垃圾桶上方
    robot.set_xyz_point(-105, 220, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到垃圾桶内
    robot.set_xyz_point(-105, 220, 100+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 释放垃圾
    robot.Servo(20)
    time.sleep_ms(1000)

    # 返回初始位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)


def move_recyclable_garbage(robot, Actuator):
    """
    其他垃圾分拣动作序列

    参数:
        robot: 机械臂控制对象
        Actuator: 执行器高度偏移量

    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到其他垃圾桶
        5. 释放垃圾并返回初始位置
    """
    print("执行可回收垃圾分拣动作...")

    # 移动到抓取准备位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 打开夹爪
    robot.Servo(10)
    time.sleep_ms(1000)

    # 进一步下降
    robot.set_xyz_point(0, 217, 10+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 用标准力度夹紧垃圾
    robot.Servo(60)
    time.sleep_ms(1000)

    # 抬升到安全高度
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 移动到其他垃圾桶上方
    robot.set_xyz_point(-120, 124, 215+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 下降到垃圾桶内
    robot.set_xyz_point(-120, 124, 100+Actuator, 0, 0)
    time.sleep_ms(1000)

    # 释放垃圾
    robot.Servo(20)
    time.sleep_ms(1000)

    # 返回初始位置
    robot.set_xyz_point(0, 174, 215+Actuator, 0, 0)
    time.sleep_ms(1000)


def execute_garbage_sorting(robot, Actuator, garbage_type):
    """
    根据垃圾类型执行相应的分拣动作

    参数:
        robot: 机械臂控制对象
        Actuator: 执行器高度偏移量
        garbage_type: 垃圾类型字符串

    支持的垃圾类型:
        - "harmful_waste": 有害垃圾
        - "kitchen_garbage": 厨余垃圾
        - "other": 其他垃圾
        - "recyclable": 可回收垃圾
    """
    if garbage_type == "harmful":
        move_harmful_waste(robot, Actuator)
    elif garbage_type == "kitchen":
        move_kitchen_garbage(robot, Actuator)
    elif garbage_type == "other":
        move_other_garbage(robot, Actuator)
    elif garbage_type == "recyclable":
        move_recyclable_garbage(robot, Actuator)
    else:
        print(f"未识别的垃圾类型: {garbage_type}")

# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com


import time

def get_piece_white(robot,Actuator,num):
    if num == 0:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 105
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 105
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 105
        robot.set_xyz_point(robotx,roboty, Actuator+30,0,0)
        time.sleep_ms(1000)

    if num == 1:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134
        robot.set_xyz_point(robotx,roboty, Actuator+60,0,0)
        time.sleep_ms(1000)

    if num == 2:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 87
        roboty = 165
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 87
        roboty = 165
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = 87
        roboty = 165
        robot.set_xyz_point(robotx,roboty, Actuator+60,0,0)
        time.sleep_ms(1000)

    if num == 3:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 193
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 193
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 193
        robot.set_xyz_point(robotx,roboty, Actuator+60,0,0)
        time.sleep_ms(1000)

    if num == 4:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 219
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 219
        robot.set_xyz_point(robotx,roboty, Actuator-15,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 219
        robot.set_xyz_point(robotx,roboty, Actuator+30,0,0)
        time.sleep_ms(1000)


def get_piece_black(robot,Actuator,num):
    if num == 0:
        robot.relay(True)
        robotx = -8
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -95
        roboty = 102
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -95
        roboty = 102
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = -95
        roboty = 102
        robot.set_xyz_point(robotx,roboty, Actuator+30,0,0)
        time.sleep_ms(1000)

    if num == 1:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -91
        roboty = 132
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -91
        roboty = 132
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = -91
        roboty = 132
        robot.set_xyz_point(robotx,roboty, Actuator+60,0,0)
        time.sleep_ms(1000)

    if num == 2:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -88
        roboty = 160
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -88
        roboty = 160
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = -88
        roboty = 160
        robot.set_xyz_point(robotx,roboty, Actuator+60,0,0)
        time.sleep_ms(1000)

    if num == 3:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -90
        roboty = 187
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -90
        roboty = 187
        robot.set_xyz_point(robotx,roboty, Actuator-18,0,0)
        time.sleep_ms(1000)
        robotx = -90
        roboty = 187
        robot.set_xyz_point(robotx,roboty, Actuator+60,0,0)
        time.sleep_ms(1000)

    if num == 4:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -87
        roboty = 213
        robot.set_xyz_point(robotx,roboty, Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -87
        roboty = 213
        robot.set_xyz_point(robotx,roboty, Actuator-16,0,0)
        time.sleep_ms(1000)
        robotx = -87
        roboty = 213
        robot.set_xyz_point(robotx,roboty, Actuator+30,0,0)
        time.sleep_ms(1000)


def move2pan(robot,Actuator,x,y):
    if x == 0 and y == 0:
        robotx = -35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = 1
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -40
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 35
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = -35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 1
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

def move2pan_45(robot,Actuator,x,y):
    if x == 0 and y == 0:
        robotx = -51
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = -23
        roboty = 230
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 0
        roboty = 253
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-5,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -23
        roboty = 185
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 25
        roboty = 230
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = 0
        roboty = 165
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 25
        roboty = 185
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 51
        roboty = 203
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)


def get_pan_piece(robot,Actuator,x,y):
    if x == 0 and y == 0:
        robotx = -35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = 1
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -40
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 35
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = -35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 1
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

def move2pan_45(robot,Actuator,x,y):
    if x == 0 and y == 0:
        robotx = -51
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = -23
        roboty = 230
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 0
        roboty = 253
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-5,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -23
        roboty = 185
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 25
        roboty = 230
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = 0
        roboty = 165
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 25
        roboty = 185
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 51
        roboty = 203
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)


def get_pan_piece(robot,Actuator,x,y):
    if x == 0 and y == 0:
        robotx = -35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = 1
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -40
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 35
        roboty = 208
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = -35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 1
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,Actuator+10,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,Actuator-10,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

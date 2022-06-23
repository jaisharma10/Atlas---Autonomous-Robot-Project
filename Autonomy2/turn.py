# ===============================================================
#                           Turn the Robot
# ===============================================================

import RPi.GPIO as GPIO
import time
import numpy as np
import serial

from sensors import readIMU, initIMU
from openMotors import init, gameover

ser = serial.Serial('/dev/ttyUSB0',9600) 

# ============================================
#                Turn Functions
# ============================================

def turnLeft(goalAngle):
    print("Going Left")
    init()
    startAngle = readIMU(ser)  # record starting orientation
    goal = startAngle - goalAngle # CCW is Positive Change

    if goal < 0:
        goal = 360 + goal
    if goal < - 360:
        goal = goal + 360
    if goal > 360:
        goal = goal - 360

    print("Start Orientation -->", startAngle, "deg")
    print("Goal Orientation -->", goal, "deg")
    # print("==============================================")
    angle = startAngle # variable updates in loop below
    val = 64

    pwmL = GPIO.PWM(33,50)
    pwmR = GPIO.PWM(37,50)

    pwmL.start(val)
    pwmR.start(val)
    
    # initialize for each turning request
    counterFL, counterBR = np.uint64(0), np.uint64(0)
    buttonFL, buttonBR = int(0), int(0)

    while(True): # angle should positively approach the goal (CCW)

        angle = readIMU(ser)
        angle = float(angle)

        # improve resolution as approaching target
        if (angle < goal + 50) and (angle > goal - 50):
            pwmL.ChangeDutyCycle(val-10)
            pwmR.ChangeDutyCycle(val-10)
            if (angle < goal + 30) and (angle > goal - 30):
                pwmL.ChangeDutyCycle(val-20)
                pwmR.ChangeDutyCycle(val-20)
                if (angle < goal + 1.5) and (angle > goal - 1.5):
                    pwmL.stop()
                    pwmR.stop()
                    gameover()
                    break

    angleChangeReal = startAngle - angle
    # print('Final Orientation:', angle, ' deg')
    # print("Orientation Error:", abs(angle - goal), 'deg')
    print("Left Turn Request Complete")
    return(angleChangeReal)

def turnRight(goalAngle):
    # print("Going Right")   
    init()

    startAngle = readIMU(ser)  # record starting orientation
    goal = goalAngle + startAngle # CCW is Positive Change

    if goal < 0:
        goal = 360 + goal
    if goal < - 360:
        goal = goal + 360
    if goal > 360:
        goal = goal - 360

    print("Start Orientation -->", startAngle, "deg")
    print("Goal Orientation -->", goal, "deg")

    # print("==============================================")

    angle = startAngle # variable updates in loop below
    val = 64

    pwmL = GPIO.PWM(31,50)
    pwmR = GPIO.PWM(35,50)

    pwmL.start(val)
    pwmR.start(val)
    
    # initialize for each turning request
    counterFL, counterBR = np.uint64(0), np.uint64(0)
    buttonFL, buttonBR = int(0), int(0)

    while(True): # angle should positively approach the goal (CCW)

        angle = readIMU(ser)
        angle = float(angle)

        # improve resolution as approaching target
        if (angle < goal + 50) and (angle > goal - 50):
            pwmL.ChangeDutyCycle(val-10)
            pwmR.ChangeDutyCycle(val-10)
            if (angle < goal + 30) and (angle > goal - 30):
                pwmL.ChangeDutyCycle(val-20)
                pwmR.ChangeDutyCycle(val-20)
                if (angle < goal + 1.5) and (angle > goal - 1.5):
                    pwmL.stop()
                    pwmR.stop()
                    gameover()
                    break
    
    angleChangeReal = startAngle - angle
    # print('Final Orientation:', angle, ' deg')
    # print("Orientation Error:", abs(angle - goal), 'deg')
    print("Right Turn Request Complete")
    return(angleChangeReal)

def turnLeftSmall(goalAngle):
    init()
    startAngle = readIMU(ser)  # record starting orientation
    goal = startAngle - goalAngle # CCW is Positive Change
    # print('Start Orientation:', startAngle, ' deg')
    # print('Goal Orientation:', goal, ' deg')
    if goal < 0:
        goal = 360 + goal
    # print('Goal Orientation:', goal, ' deg')


    angle = startAngle # variable updates in loop below
    val = 35

    pwmL = GPIO.PWM(33,50)
    pwmR = GPIO.PWM(37,50)
    pwmL.start(val)
    pwmR.start(val)
    
    # initialize for each turning request
    counterFL, counterBR = np.uint64(0), np.uint64(0)
    buttonFL, buttonBR = int(0), int(0)

    while(True): # angle should positively approach the goal (CCW)

        angle = readIMU(ser)
        angle = float(angle)

        if (angle < goal + 3) and (angle > goal - 3):
            pwmL.stop()
            pwmR.stop()
            gameover()
            break
    
    angleChangeReal = startAngle - angle
    # print('Final Orientation:', angle, ' deg')
    # print("Orientation Error:", abs(angle - goal), 'deg')
    # print("Small Left Turn Request Complete")
    return(angleChangeReal)

def turnRightSmall(goalAngle):
    init()
    startAngle = readIMU(ser)  # record starting orientation
    goal = startAngle + goalAngle # CCW is Positive Change
    # print('Start Orientation:', startAngle, ' deg')
    # print('Goal Orientation:', goal, ' deg')
    if goal < 0:
        goal = 360 + goal
    angle = startAngle # variable updates in loop below
    val = 35
    # print('Goal Orientation:', goal, ' deg')

    pwmL = GPIO.PWM(31,50)
    pwmR = GPIO.PWM(35,50)
    pwmL.start(val)
    pwmR.start(val)
    
    # initialize for each turning request
    counterFL, counterBR = np.uint64(0), np.uint64(0)
    buttonFL, buttonBR = int(0), int(0)

    while(True): # angle should positively approach the goal (CCW)

        angle = readIMU(ser)
        angle = float(angle)

        if (angle < goal + 3) and (angle > goal - 3):
            pwmL.stop()
            pwmR.stop()
            gameover()
            break

    angleChangeReal = startAngle - angle
    # print('Final Orientation:', angle, ' deg')
    # print("Orientation Error:", abs(angle - goal), 'deg')
    # print("Small Right Turn Request Complete")
    return(angleChangeReal)
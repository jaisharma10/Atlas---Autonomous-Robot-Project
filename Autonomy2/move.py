# ===============================================================
#                           Move the Robot
# ===============================================================

import RPi.GPIO as GPIO
import time
import numpy as np
from openMotors import init, gameover

# ============================================
#                 Initialization
# ============================================

# wheel and encoder variables
circf = 2 * np.pi * 32.5        # in mm
ticksPerRev = 20 * 2            # combined counts
const = ticksPerRev/circf

# ============================================
#               Estimate Distance
# ============================================

# estimates distance to trav
def getDistance(radius):
    if radius > 0 and radius < 41:
        power = 1/(-0.847)
        distance = (radius/5087.6)**power
        if distance > 750:
            distance = 500
        else:
            distance = distance - 150
    elif  radius > 40 and radius < 46:
         distance = 100
    else:
        distance = 50
    return(distance)

# ============================================
#               PID Correction
# ============================================

def correction(counterBR,counterFL, prevError, sumError, pwmL, pwmR, makeList):
    
    kp = 1/1000
    kd = kp / 2
    ki = kd / 2

    val = 50
    error = counterBR - counterFL     # PID based correction
    abs_error = abs(error)
    # print("SumError:", sumError)
    if sumError > 5000:
        sumError = sumError/2
    if sumError < -5000:
        sumError = sumError/2
    correction = (abs_error*kp) + (prevError*kd) + (sumError*ki)     # print("Error in Encoder Counts:", error)
    # print("Error:", round(error,5))
    # print("Correction:", round(correction,3))
    makeList.append(round(error,2))
    pwmAdd = val - correction
    pwmRed = val + correction

    if pwmAdd < 0:
        pwmAdd = 0
    if pwmAdd > 100:
        pwmAdd = 100
    
    if pwmRed < 0:
        pwmRed = 0
    if pwmRed > 100:
        pwmRed = 100

    # print("pwmAdd: ", pwmAdd, "|| pwmRed: ", pwmRed)

    if (error > 0): # right count is bigger
        pwmL.ChangeDutyCycle(pwmAdd)
        pwmR.ChangeDutyCycle(pwmRed)
    elif (error < 0): # left count is bigger
        pwmL.ChangeDutyCycle(pwmRed)
        pwmR.ChangeDutyCycle(pwmAdd)
    else:
        pwmL.ChangeDutyCycle(val)
        pwmR.ChangeDutyCycle(val)

    prevError = error
    sumError += error

    return(prevError, sumError, makeList)

# ============================================
#             Direction Functions
# ============================================

def forward(goalDistance):
    init()
    distance = 0
    # initialize for each turning request
    counterFL, counterBR = np.uint64(0), np.uint64(0)
    buttonFL, buttonBR = int(0), int(0)
    pwmL = GPIO.PWM(31,50)       # left wheel pins
    pwmR = GPIO.PWM(37,50)       # right wheel pins
    val = 60
    pwmL.start(val)
    pwmR.start(val)
    # PID vairables
    prevError, sumError = 0, 0
    makeList = []
    # start loop till goal reached
    while(distance < goalDistance):
        pwmL.ChangeDutyCycle(val)
        pwmR.ChangeDutyCycle(val)
        if int(GPIO.input(12)) != int(buttonFL):
            buttonFL = int(GPIO.input(12))      # tracks pin state
            counterFL += 1                      # counts number of ticks
        if int(GPIO.input(7)) != int(buttonBR):
            buttonBR = int(GPIO.input(7))
            counterBR += 1
            # print("Left Ticks:", counterFL, "    ||    Right Ticks:", counterBR)
        distance = (counterBR + counterFL) / const
        # PID correction here
        prevError, sumError, makeList = correction(counterBR,counterFL, prevError, sumError, pwmL, pwmR, makeList)
    
    # print("Final Left Ticks:", counterFL, "    ||    Final Right Ticks:", counterBR)
    # print("Distance Travelled: ", round(distance, 3), " mm")
    # print("prevError", prevError)
    # print("sumError", sumError)
    # print("Correction List", makeList)

    pwmL.stop()
    pwmR.stop()
    gameover()
    return(None)

def reverse(goalDistance):
    init()
    distance = 0
    # initialize for each turning request
    counterFL, counterBR = np.uint64(0), np.uint64(0)
    buttonFL, buttonBR = int(0), int(0)
    pwmL = GPIO.PWM(33,50)       # left wheel pins
    pwmR = GPIO.PWM(35,50)       # right wheel pins
    val = 25
    pwmL.start(val)
    pwmR.start(val)
    # PID vairables
    prevError, sumError = 0, 0
    makeList = []
    # start loop till goal reached
    while(distance < goalDistance):
        pwmL.ChangeDutyCycle(val)
        pwmR.ChangeDutyCycle(val)
        if int(GPIO.input(12)) != int(buttonFL):
            buttonFL = int(GPIO.input(12))      # tracks pin state
            counterFL += 1                      # counts number of ticks
        if int(GPIO.input(7)) != int(buttonBR):
            buttonBR = int(GPIO.input(7))
            counterBR += 1
        # print("Left Ticks:", counterFL, "    ||    Right Ticks:", counterBR)
        distance = (counterBR + counterFL) / const
        # print("Distance: ", round(distance, 3), " mm")
        # PID correction here
        # prevError, sumError, makeList = correction(counterBR,counterFL, prevError, sumError, pwmL, pwmR, makeList)
    
    # print("Final Left Ticks:", counterFL, "    ||    Final Right Ticks:", counterBR)
    # print("Distance: ", round(distance, 3), " mm")
    # print("prevError", prevError)
    # print("sumError", sumError)
    # print("Correction List", makeList)

    pwmL.stop()
    pwmR.stop()
    gameover()
    return(None)

def goforward(tf):
    init()
    GPIO.output(31, True)    # Left Wheels
    GPIO.output(33, False)
    GPIO.output(35, False)     # Right Wheels
    GPIO.output(37, True)
    time.sleep(tf)     # Wait
    gameover()


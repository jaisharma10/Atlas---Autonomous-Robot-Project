# =====================================================
#                    Sensor Functions
# =====================================================

import serial
import RPi.GPIO as GPIO
import time

def initIMU(ser):
    count = 0
    while(count < 11):
        line = ser.readline()
        line = line.rstrip().lstrip()
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        line = line.strip("X")
        line = line.strip(":")
        line = line.strip("\\x")
        line = line.strip("/")
        try:
            angle = float(line)
            # print("current angle --> ", angle, "deg") 
            count += 1
        except:
            pass
    # print("initial angle --> ", angle, "deg") 
    return(angle)

def readIMU(ser):
    while(True):
        line = ser.readline()
        line = line.rstrip().lstrip()
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        line = line.strip("X")
        line = line.strip(":")
        line = line.strip("\\x")
        line = line.strip("/")
        try:
            angle = float(line)
            # print("current angle --> ", angle, "deg") 
            break
        except:
            pass
    return(angle)


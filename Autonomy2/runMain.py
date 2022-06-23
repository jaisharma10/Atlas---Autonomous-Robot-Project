# =====================================================
#                    Main File
# =====================================================

import time
import serial

from openMotors import init, gameover
from actionModes import getBlock, mode1, checkMasks
from turn import turnRight, turnLeft, turnLeftSmall, turnRightSmall
from sensors import initIMU, readIMU
from sendEmail import sendit
from move import getDistance, forward, goforward, reverse


ser = serial.Serial('/dev/ttyUSB0',9600) 

if __name__ == '__main__':
    
    startTime = time.time()
    print("Start Now")

    mode1()

    for index in range(3):   
        print("Getting Red x-x-x-x-x-x-x-x-x-xx-x-x-x-x-x-x-x-x-xx-x-x-x-x-x-x-x-x-x")
        getBlock(1)
        print("Getting Green x-x-x-x-x-x-x-x-x-xx-x-x-x-x-x-x-x-x-xx-x-x-x-x-x-x-x-x-x")
        getBlock(2)
        print("Getting Blue x-x-x-x-x-x-x-x-x-xx-x-x-x-x-x-x-x-x-xx-x-x-x-x-x-x-x-x-x")
        getBlock(3)

    init()
    gameover()

    endTime = time.time()
    runTime = endTime - startTime
    print("Gameover")
    print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(runTime)))

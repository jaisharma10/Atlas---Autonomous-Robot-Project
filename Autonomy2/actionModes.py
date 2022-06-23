# =====================================================
#                    Camera Functions
# =====================================================

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import imutils
import time
import RPi.GPIO as GPIO
import serial

from move import getDistance, forward, goforward, reverse
from gripper import gripperClose, gripperOpen
from openMotors import init, gameover
from perception import AoI_mask, redMask, greenMask, blueMask, getCircles, getPointer, alignBlock
from sensors import readIMU
from turn import turnLeft, turnRight, turnLeftSmall, turnRightSmall
# from sendEmail import sendit

# # send email to Professor
# sendit()

ser = serial.Serial('/dev/ttyUSB0',9600) 

# =====================================================
#                    Initialization
# =====================================================

# Camera Initialization
camSz = (640, 480)
cols,rows = camSz[0], camSz[1]
camera = PiCamera()
camera.resolution = camSz 
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=camSz)
time.sleep(5)

def checkMasks():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = False):
        image = frame.array
        image = cv2.flip(image, -1) 
        imgCenter = int(image.shape[1] / 2) # get center of block
        # --------------------- detect the block -----------------------------
        red_mask = redMask(image)           # red HSV Mask
        blue_mask = blueMask(image)           # blue HSV Mask
        green_mask = greenMask(image)           # blue HSV Mask
        output, radius, center = getCircles(image, red_mask)  # plot circles around biggest Block
        travel = getDistance(radius)      # estimates distance to travel based on radius
        print("Distance to Travel Estimate:", round(travel, 3), "mm")
        error = (center[0] - imgCenter)  # orientation error
        cv2.putText(output, 'Error: ' + str(error), (500, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_4) 
        # output, error = alignBlock(output, radius, center)   # align the robot with the block
        output = getPointer(output)            # get cross mark on image
        cv2.imshow("Circles", output)
        cv2.imshow("red_mask", red_mask)
        cv2.imshow("blue_mask", blue_mask)
        cv2.imshow("green_mask", green_mask)

        rawCapture.truncate(0)
        # break the loop conditions
        if cv2.waitKey(1) == ord('q'):
            break      

    cv2.destroyAllWindows()
    return(None)

def mode1():
    forward(2730)
    time.sleep(1)
    turnRight(90)
    forward(100)

def getBlock(blockNumber):

    startAngle = readIMU(ser)
    print("Start Orientation:", startAngle)
    endLoop = False
    travelTot = 0
    angleAdjust = 0
    homePosAdjust = 0
    exploreCount = 0

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = False):
        image = frame.array
        image = cv2.flip(image, -1) 
        # cv2.imshow("Image", image) # displays original image

        # --------------------- get appropriate hsv mask -----------------------------
        
        if blockNumber == 1:
            red_mask = redMask(image)           # red HSV Mask
            outputImg, radius, center = getCircles(image, red_mask)  # plot circles around biggest Block
            mask = red_mask
            # print("Retrieving Red Block")

        elif blockNumber == 2:
            green_mask = greenMask(image)           # green HSV Mask
            outputImg, radius, center = getCircles(image, green_mask)  # plot circles around biggest Block
            mask = green_mask
            # print("Retrieving Green Block")

        elif blockNumber == 3:
            blue_mask = blueMask(image)           # blue HSV Mask
            outputImg, radius, center = getCircles(image, blue_mask)  # plot circles around biggest Block
            mask = blue_mask
            # print("Retrieving Blue Block")

        # -------------------- detect the block ---------------------------
        output, error, realAngChange, radius = alignBlock(outputImg, radius, center)   # align the robot with the block
        
        # update orientation changes here
        if travelTot == 0: # if still at origin
            homePosAdjust += realAngChange
            print("homePosAdjust", homePosAdjust)
        else: # if yaw change is during approach
            if angleAdjust == 0:
                approachAng = readIMU(ser)
                print("xoxoxox Approach Orientation", approachAng)   
            angleAdjust += realAngChange
            print("angleAdjust", angleAdjust)

        output = getPointer(output)            # display cross mark on image
        cv2.imshow("Circles", output)
        cv2.imshow("mask image", mask)
        
        # ----------------- explore if no block detected -----------------------

        if radius == 0:
            if exploreCount < 3:
                print("Looking for Block")
                initChange = turnRightSmall(20)
                # homePosAdjust += initChange
                exploreCount += 1
            else:
                initChange = turnLeft(90)
                forward(250)
                angleAdjust += initChange
                travelTot += 250 
                exploreCount = 0

        # -------------------- go towards the block ---------------------------
      
        # Fast Approach
        if (abs(error) < 91) and (radius < 50):
            gripperClose()
            travelFast = getDistance(radius) * 3/4      # estimates distance to travel based on radius
            forward(travelFast)                  # travels to the block            readIMU(ser)
            travelTot += travelFast

        # Slow Approach
        if (abs(error) < 71) and (radius > 49 and radius < 121) :
            gripperOpen()
            travelSlow = 60
            forward(travelSlow)             # get closer slowly
            travelTot += travelSlow
   
        # -------------------- pick up block and retrieve ---------------------------

        # Pick Up Manoeuvre 
        if (abs(error) < 101) and (radius > 120):
            gripperOpen()
            travelPickUp = 110
            forward(travelPickUp)             # get closer enough to pick up
            gripperClose()

            # Note pick up angle
            pickUpAngle = readIMU(ser)
            print("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
            print("Orientation at Pick Up", pickUpAngle)

            travelTot += travelPickUp

            # -------------------- fix orientation ---------------------------

            turnLeft(abs(startAngle - pickUpAngle))  # reach HomeOrientation
            time.sleep(2)
            turnLeft(180 - abs(homePosAdjust))  # face the origin from pick up point
            time.sleep(2)

            returnAng = readIMU(ser)
            print("xoxoxox Returning Orientation", returnAng)

            # -------------------- return to origin and drop block ---------------------------

            travelTot = travelTot + 200
            if travelTot > 1000:
                travelTot += 200

            forward(travelTot) 
            time.sleep(0.5)
            gripperOpen()

            # -------------------- go to Home Position ---------------------------

            travelRev = 200
            reverse(travelRev)

            print("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")

            print("xoxoxox Start Orientation", startAngle)
            dropAngle = readIMU(ser)  # get orientation after drop off
            print("xoxoxox Drop Off Orientation", dropAngle)
            print("xoxoxox dropAngle - startAngle", dropAngle - startAngle)
            turnRight(startAngle + (360 - dropAngle)) 

            endLoop = True

        
        
        
        # -------------------------------------------------------------------

        rawCapture.truncate(0)
        if endLoop == True:
            break

        # break the loop conditions
        if cv2.waitKey(1) == ord('q'):
            break      

    cv2.destroyAllWindows()
    return(None)

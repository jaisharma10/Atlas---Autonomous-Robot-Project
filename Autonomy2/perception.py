# ==============================================
#             Mask Related Functions
# ==============================================

import cv2
import numpy as np
import imutils
from turn import turnLeft, turnRight, turnLeftSmall, turnRightSmall

def AoI_mask(image):
    h, w = image.shape[0], image.shape[1]
    vertices = np.array([[(0,h/2), (w,h/2), (w,h), (0,h)]], np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, (255, 255, 255))
    maskImg = cv2.bitwise_and(image, mask)
    return(maskImg)
 
def redMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    red_lower = np.array([150,110,20]) # 162,184,20
    red_upper = np.array([180,255,255]) # 183, 255, 255
    getRed = cv2.inRange(hsv, red_lower, red_upper)
    return(getRed)

def greenMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    green_lower = np.array([50,60, 30])
    green_upper = np.array([80, 255, 255])
    getGreen = cv2.inRange(hsv, green_lower, green_upper)
    return(getGreen)

def blueMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue_lower = np.array([100, 120, 80])
    blue_upper = np.array([130, 255, 255])
    getBlue = cv2.inRange(hsv, blue_lower, blue_upper)
    return(getBlue)

def getCircles(original, mask):
    # find contours 
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center, radius = (0, 0), 0
    # detect and cicle biggest contour in frame
    try:
        for c in contours:
            M = cv2.moments(c) #cv2.moments for the center
            if M["m00"] != 0:
                cX, cY = int(M["m10"] / M["m00"]),  int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            c_max = max(contours, key = cv2.contourArea)
            (x,y),radius = cv2.minEnclosingCircle(c_max)
            center, radius = (int(x),int(y)), int(radius)
        if radius > 2:
            cv2.circle(original, center, radius, (0,250,250), 3)
    except:
        pass

    # Didplay Radius and Center information
    cv2.putText(original, 'Radius: ' + str(radius), (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2, cv2.LINE_4)
    cv2.putText(original, 'Center: ' + str(center), (400, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_4) 
    
    return(original, radius, center)

def alignBlock(image, radius, center):
    print("Change")
    imgCenter = int(image.shape[1] / 2) # get center of block
    x = center[0]   # default value
    buffer = 40     # pixels
    # Act if block in this range
    actualChange = 0

    error = (x - imgCenter)  # orientation error
    cv2.putText(image, 'Error: ' + str(error), (500, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_4) 
 
    angle = 5 if abs(error) > 70 else 2

    if (radius > 0):
        if int(x) > (imgCenter + buffer):
            # print("left")
            actualChange = turnRightSmall(angle)  # attempt the turn and record actual change
        elif int(x) < (imgCenter - buffer):
            actualChange = turnLeftSmall(angle)
            # print("red")

    # print(actualChange)
    return(image, error, actualChange, radius)

def getPointer(image):
    a = int(image.shape[0] - image.shape[0] / 3)
    b = int(image.shape[1] / 2)
    cv2.line(image,(b, a + 100),(b, a - 100),(0,255,0),4)
    cv2.line(image,(b + 60, a),(b - 60, a),(0,255,0),4)
    return(image)
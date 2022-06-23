# =====================================================
#              Gripper Functions  
# =====================================================

import RPi.GPIO as GPIO
import time

# Add Email Functionalities

def gripperOpen():
    val = 8
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(36, GPIO.OUT) # Servo Pin
    pwm = GPIO.PWM(36, 50)
    pwm.start(val)
    time.sleep(2)
    # pwm.stop()
    # GPIO.cleanup()
    return(None)

def gripperClose():
    val = 2
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(36, GPIO.OUT) # Servo Pin
    pwm = GPIO.PWM(36, 50)
    pwm.start(val)
    time.sleep(2)
    pwm.stop()
    GPIO.cleanup()
    return(None)
# ==============================================
#                   Open Motors
# ==============================================

import RPi.GPIO as GPIO
import time

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(31, GPIO.OUT) 
    GPIO.setup(33, GPIO.OUT) 
    GPIO.setup(35, GPIO.OUT) 
    GPIO.setup(37, GPIO.OUT) 
    GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def gameover():
    # Set all pins LOW
    GPIO.output(31, False)
    GPIO.output(33, False)
    GPIO.output(35, False)
    GPIO.output(37, False)
    # GPIO.cleanup()

if __name__ == '__main__':
    init()
    gameover()
import RPi.GPIO as gpio
import time, sys
import easydriver as ed

def spin():
    # GPIO Setup
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    # GPIO Pin Setup
    gpio.setup(18, gpio.OUT)

    # EasyDriver init           Speed
    stepper = ed.easydriver(18, 0.005, 23, 24, 17, 25)

    # Spin Once
    count = 0
    while count < 1600 :
            stepper.step()
            count += 1


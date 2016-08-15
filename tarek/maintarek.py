import serial
import time
import sys
import classr

# main
ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)

robot = classr.Roomba()
robot._start()
robot._safe()
time.sleep(3)
robot._clean()
time.sleep(10)
robot._safe()
time.sleep(3)
robot._clean()
time.sleep(10)
robot._safe()

import serial
import time
import sys

# main....
ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)

print("Starting interface")
ser.write(chr(128))
time.sleep(0.1)
print("Roomba is ready if it just beeped")
ser.write(chr(131))
time.sleep(0.1)
print("Start cleaning")
ser.write(chr(135))
time.sleep(0.1)


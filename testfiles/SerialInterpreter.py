# 
# SerialInterpreter.py
# 
# Roomba-Control 
# New York University (c) 2016
# 

import serial
import time
import sys

class SerialInterpreter:
    # Serial Constants

    SERIAL_INTERFACE = "/dev/ttyAMA0"
    BAUD_RATE = 115200

    # Opcode Constants

    # PLACE OPCODE CONSTANTS HERE

    def __init__(self):
        print("Starting serial communction on " + SERIAL_INTERFACE " at " BAUD_RATE "baud")
        serialConnection = serial.Serial(SERIAL_INTERFACE,baudrate = BAUD_RATE,timeout = 0.1)

        pass

    def sendOpcode(opcode):
        print("Sending command with opcode: " + str(opcode))
        serialConnection.write(chr(opcode))
        time.sleep(0.1)

    def readFromSerial(opcode):
        print("Invoking read with opcode: " + str(opcode))
        # PLACE IMPLEMENTATION FOR
        # READING SERIAL HERE

        # Return the bytes received
        return 0




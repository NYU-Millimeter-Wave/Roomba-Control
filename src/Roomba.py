#!/usr/bin/env/python

import os
import signal
import time
import math
import serial
from multiprocessing import Process

class Roomba:

    ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
    ser.flushInput()

    SPEED = 200

    def __init__(self):
        # Motor priming
        print("Roomba Init")
        self.start()
        self.safe()
        self.stop()
        self.bumpLeft = False
        self.bumpRight = False

        # Spawn sensor listener
        self.startBumpListener()

        print("Roomba is ready")

    def startBumpListener(self):
        print("Spawning bump listener loop...")
        self.bumpLoop = Process(target=self.watchBump)
        self.bumpLoop.start()
        print("Spawned with pid " + str(self.bumpLoop.pid))

    def stopBumpListener(self):
        print ("Stopping bump listener")
        self.bumpLoop.terminate()

    def watchBump(self):
        while True:
            self.getBumps()
            time.sleep(0.15)
            if self.bumpRight == True:
                print("Bumped Right")
                self.backward()
                time.sleep(0.5)
                self.turn()
                self.forward()
            elif self.bumpLeft == True:
                print("Bumped Left")
                self.backward()
                time.sleep(0.5)
                self.turnLeft()
                self.forward()

    # Drive Methods

    def drive(self,vel,rad):
        (vel_high, vel_low) = self.toHex(vel)
        (radius_high, radius_low) = self.toHex(rad)
        self._write( chr(137) )
        self._write( chr(vel_high) )
        self._write( chr(vel_low) )
        self._write( chr(radius_high) )
        self._write( chr(radius_low) )
        return

    # def forward(self):
        # print("Forward...")
        # (vel_high, vel_low) = self.toHex(200)
        # (radius_high, radius_low) = self.toHex(0)
        # self._write( chr(137) )
        # self._write( chr(vel_high) )
        # self._write( chr(vel_low) )
        # self._write( chr(radius_high) )
        # self._write( chr(radius_low) )
        # return

    def forward(self):
        print("Forward...")
        self.drive(self.SPEED, 0)

    def backward(self):
        print("Backward...")
        self.drive((self.SPEED * -1), 0)

    def taperStop(self):
        currSpeed = self.SPEED
        while currSpeed > 0:
            (vel_high, vel_low) = self.toHex(currSpeed)
            (radius_high, radius_low) = self.toHex(currSpeed)
            self._write( chr(137) )
            self._write( chr(vel_high) )
            self._write( chr(vel_low) )
            self._write( chr(radius_high) )
            self._write( chr(radius_low) )
            currSpeed -= 1
        self.stop()
        print("Stopped")
        return

    def stop(self):
        print("Stopped")
        (vel_high, vel_low) = self.toHex(0)
        (radius_high, radius_low) = self.toHex(0)
        self._write( chr(137) )
        self._write( chr(vel_high) )
        self._write( chr(vel_low) )
        self._write( chr(radius_high) )
        self._write( chr(radius_low) )
        return

    def turn(self):
        print("Turning...")
        angle = -1
        self.drive(self.SPEED,angle)
        # 0.54 = 90 deg
        time.sleep(0.54)
        return

    def turnLeft(self):
        print("Turning Left...")
        angle = 1
        self.drive(self.SPEED,angle)
        # 0.54 = 90 deg
        time.sleep(0.54)
        return

    # Sensor Methods

    def getStasis(self):
        self._write( chr(142) )
        self._write( chr(58) )
        resp2 = self.ser.read(1)
        s = (int((resp2).encode('hex'), 16))
        #print ('stasis='+str(s))
        return s

    def getBumps(self):
        self._write( chr(142) )
        self._write( chr(7) )
        resp = self.ser.read(1)
        respHex = int(resp.encode('hex'), 16)

        # Bit Masking      NA RGT LFT
        maskRight = 0x38 # 00 111 000
        maskLeft  = 0x7  # 00 000 111

        respRight = respHex & maskRight
        respLeft  = respHex & maskLeft

        if respRight != 0 :
            self.bumpRight = True
        else:
            self.bumpRight = False
        if respLeft != 0 :
            self.bumpLeft = True
        else:
            self.bumpLeft = False
        return

    # Mode Methods

    def driveDirect(self):
        print("In drive direct mode")
        self._write( chr(145) )
        time.sleep(0.25)
        return

    def start(self):
        print("Starting...")
        self._write( chr(128) )
        # 20 ms between mode-changing commands
        time.sleep(0.25)
        return

    def safe(self):
        print("In safe mode")
        self._write( chr(131) )
        # 20 ms between mode-changing commands
        time.sleep(0.25)
        return

    def _write(self,byte):
        self.ser.write(byte)
        return

    # Utility Methods

    def toHex(self, value):
        """ returns two bytes (ints) in high, low order
        whose bits form the input value when interpreted in
        two's complement
        """
        if value >= 0:
            eqBitVal = value
        else:
            eqBitVal = (1<<16) + value

        return ( (eqBitVal >> 8) & 0xFF, eqBitVal & 0xFF )

    # Teardown Function

    def term(self):
        print("Roomba: SIGINT received, exiting...")
        os.kill(self.bumpLoop.pid, signal.SIGTERM)
        self.stop()
        self.safe()
        self.ser.flushInput()
        self.ser.close()


#!/usr/bin/env/python

import time
import math
import serial
import signal
from multiprocessing import Process

class Roomba:

    ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
    ser.flushInput()

    def __init__(self):
        # Motor priming
        print("Roomba Init")
        self.start()
        self.safe()
        self.stop()
        self.stasis = False

        # Spawn sensor listener
        print("Spawning stasis listener loop...")
        self.stasisLoop = Process(target=self.watchStasis).start()
        print("Spawned with pid " + self.stasisLoop.pid)

        # Init proc signal listener
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()

        print("Roomba is ready")

    def watchStasis(self):
        while True:
            self.stasis = self.getStasis()
            print("Current Stasis:" + self.stasis)
            time.sleep(0.20)
            if self.stasis == 0:
                self.drive(-500, 0)
                time.sleep(0.5)
                self.turn()
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

    def forward(self):
        print("Forward...")
        (vel_high, vel_low) = self.toHex(500)
        (radius_high, radius_low) = self.toHex(0)
        self._write( chr(137) )
        self._write( chr(vel_high) )
        self._write( chr(vel_low) )
        self._write( chr(radius_high) )
        self._write( chr(radius_low) )
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
        self.drive(500,angle)
        # 0.54 = 90 deg
        time.sleep(0.54 / 2)
        return

    # Sensor Methods

    def getStasis(self):
        self._write( chr(142) )
        self._write( chr(58) )
        resp2 = self.ser.read(1)
        s = (int((resp2).encode('hex'), 16))
        #print ('stasis='+str(s))
        return s

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

    def signal_handler(signal, frame):
        print("Roomba: SIGINT received, exiting...")
        self.stasisLoop.terminate()
        sys.exit(0)

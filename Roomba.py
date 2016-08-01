#!/usr/bin/env/python

import time
import math
import serial

class Roomba(object):

    START       = chr(128)
    SENSORS     = chr(142)
    STASIS      = chr(58)
    DRIVEDIRECT = chr(145)
    SAFE_MODE   = 2

    ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)

    def __init__(self):
        print("Roomba Init")
        self._start()
        self._driveDirect()
        self.stop()

    # Drive Methods

    def forward(self):
        (vel_high, vel_low) = self.toHex(50)
        (radius_high, radius_low) = self.toHex(0)
        self._write( chr(137) )
        self._write( chr(vel_high) )
        self._write( chr(vel_low) )
        self._write( chr(radius_high) )
        self._write( chr(radius_low) )
        #time.sleep(0.25)
        return

    def stop(self):
        (vel_high, vel_low) = self.toHex(0)
        (radius_high, radius_low) = self.toHex(0)
        self._write( chr(137) )
        self._write( chr(vel_high) )
        self._write( chr(vel_low) )
        self._write( chr(radius_high) )
        self._write( chr(radius_low) )
        # time.sleep(0.25)
        return

    def turn(self):
        self.stop()
        angle = -1
        self.drive(500,angle)
        # 0.25 seconds = 90°
        time.sleep(0.25 / 2)
        self.stop()
        return

    # Sensor Methods

    def getStasis(self):
        self._write( SENSORS )
        self._write( STASIS )
        resp2 = self.ser.read(1)
        s = (int((resp2).encode('hex'), 16))
        #print ('stasis='+str(s))
        return s

    # Mode Methods

    def _driveDirect(self):
        self.write( DRIVEDIRECT )
        time.sleep(0.25)
        return
    
    def _start(self):
        self._write( START )
        # 20 ms between mode-changing commands
        time.sleep(0.25)
        return
    
    def _safe(self):
        self._write( SAFE )
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

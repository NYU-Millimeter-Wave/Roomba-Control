#!/usr/bin/env/python

import time
import math
import serial
from Roomba import Roomba

def test():
    roomba = Roomba()
    #roomba.forward()
    #time.sleep(2)
    #roomba.stop()
    #roomba.turn()
    #roomba.forward()
    #time.sleep(2)
    #roomba.stop()
    #roomba.safe()

    while(True):
        stasis = roomba.getStasis()
        if stasis == 0:
            roomba.turn()
        roomba.forward()
        time.sleep(0.25)

if __name__ == '__main__':
    test()



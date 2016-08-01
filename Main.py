#!/usr/bin/env/python

import Roomba

if __name__ == '__main__':
    roomba = Roomba()
    roomba.forward()
    
    while(True):
        stasis = roomba.getStasis()
        if stasis == 1:
            roomba.turn()
            roomba.forward()
        time.sleep(0.25)


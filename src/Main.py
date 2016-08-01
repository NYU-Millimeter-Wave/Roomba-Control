#!/usr/bin/env/python

import time
import math
import serial
import os
from Roomba import Roomba

global roomba

if __name__ == '__main__':
    os.system("sudo python RoombaTCPServer.py &")
    os.system("sudo python RoombaHTTPServer.py &")
    roomba = Roomba.Roomba()


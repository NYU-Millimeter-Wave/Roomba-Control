#!/usr/bin/env/python

import os
import sys
import subprocess
import signal
from Roomba import Roomba

global roomba
global tcpProc
global httpProc

def signal_handler(signal, frame):
    print("\nMain: SIGINT received, exiting...")
    teardown()

def teardown():
    tcpProc.terminate()
    httpProc.terminate()
    roomba.term()
    sys.exit(0)

if __name__ == '__main__':

    # Initialize Roomba control object
    roomba = Roomba()

    print("Creating child processes...")

    tcpProc  = subprocess.Popen(['python src/RoombaTCPServer.py'], shell=True)
    httpProc = subprocess.Popen(['python src/RoombaHTTPServer.py'], shell=True)

    print("TCP server spawned with pid " + str(tcpProc.pid))
    print("HTTP server spawned with pid " + str(httpProc.pid))

    # Init proc signal listener
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    # # Spawn TCP Process
    # os.system("sudo python src/RoombaTCPServer.py &")

    # # Spawn HTTP Process
    # os.system("sudo python src/RoombaHTTPServer.py &")


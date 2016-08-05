#!/usr/bin/env/python

import os
import sys
import subprocess
import signal
from Roomba import Roomba

global tcpProc
global httpProc

def signal_handler(signal, frame):
    print("\nMain: SIGINT received, exiting...")
    tcpProc.terminate()
    httpProc.terminate()
    sys.exit(0)

if __name__ == '__main__':

    # Initialize Roomba control object
    print("Creating child processes...")

    tcpProc  = subprocess.Popen(['python src/RoombaTCPServer.py'], shell=True)
    httpProc = subprocess.Popen(['python src/RoombaHTTPServer.py'], shell=True)

    print("TCP server spawned with pid " + str(tcpProc.pid))
    print("HTTP server spawned with pid " + str(httpProc.pid))

    # Init proc signal listener
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()


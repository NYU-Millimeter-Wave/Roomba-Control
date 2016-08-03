#!/usr/bin/env/python

import os
import sys
import subprocess
import signal
from Roomba import Roomba

global roomba

def signal_handler(signal, frame):
    print("Main: SIGINT received, exiting...")
    teardown()

def teardown():
    roomba.term()
    proc.terminate()
    proc2.terminate()
    sys.exit(0)

if __name__ == '__main__':

    # Initialize Roomba control object
    roomba = Roomba()

    print("Creating child processes...")

    proc  = subprocess.Popen(['python src/RoombaTCPServer.py'], shell=True)
    proc2 = subprocess.Popen(['python src/RoombaHTTPServer.py'], shell=True)

    print("TCP server spawned with pid " + str(proc.pid))
    print("HTTP server spawned with pid " + str(proc2.pid))

    # Init proc signal listener
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    # # Spawn TCP Process
    # os.system("sudo python src/RoombaTCPServer.py &")

    # # Spawn HTTP Process
    # os.system("sudo python src/RoombaHTTPServer.py &")


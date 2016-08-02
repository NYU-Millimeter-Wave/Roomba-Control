#!/usr/bin/env/python

import os
import subprocess
import signal
from Roomba import Roomba

global roomba

def signal_handler(signal, frame):
    print("Main: SIGINT received, exiting...")
    sys.exit(0)

if __name__ == '__main__':

    # Initialize Roomba control object
    roomba = Roomba()

    print("Creating child processes...")

    proc  = subprocess.Popen(['sudo', 'python', 'src/RoombaTCPServer.py'], shell=True)
    proc2 = subprocess.Popen(['sudo', 'python', 'src/RoombaHTTPServer.py'], shell=True)

    print("TCP server spawned with pid " + proc.pid)
    print("HTTP server spawned with pid " + proc2.pid)

    # Init proc signal listener
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    # # Spawn TCP Process
    # os.system("sudo python src/RoombaTCPServer.py &")

    # # Spawn HTTP Process
    # os.system("sudo python src/RoombaHTTPServer.py &")


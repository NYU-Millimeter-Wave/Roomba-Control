#!/usr/bin/env/python

import signal
import sys
import os
import socket
import Spin
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleHandler(WebSocket):

    def handleMessage(self):
        print("Message Received: " + str(self.data))
        if str(self.data) == "SHUTDOWN":
            print("Shutdown signal received, exiting...")
            self.close()
            sys.exit(0)

        if str(self.data) == "START":
            print("Signalled to begin")
            self.sendMessage(unicode('VSTART'))
            # START MAIN PROGRAM
            # os.system(RoombaControl.py)

        if str(self.data) == "READING":
            print("Signalled to read, stopping movement")
            self.sendMessage(unicode('VREADING'))
            # STOP ROVER MOVEMENT
            print("Movement halted")

        if str(self.data) == "READNOW":
            print("Taking reading...")
            self.sendMessage(unicode('VREADNOW'))
            Spin.spin()
            print("Done taking reading")

        if str(self.data) == "ENDEXP":
            print("Signalled End of experiment")
            # RUN CLEAN UP SCRIPTS

    def handleConnected(self):
        print("New Connection: " + str(self.address))

    def handleClose(self):
        print("Closed Connection: " + str(self.address))

def signal_handler(signal, frame):
    print("SIGINT received, exiting...")
    server.close()
    sys.exit(0)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

if __name__ == '__main__':
    port = 9000
    # ipaddr = socket.gethostbyname(socket.gethostname())
    ipaddr = get_ip_address()
    server = SimpleWebSocketServer(str(ipaddr), port, SimpleHandler)
    print("Serving TCP Socket on " + str(ipaddr) + ":" + str(port))

    signal.signal(signal.SIGINT, signal_handler)
    server.serveforever()
    signal.pause()

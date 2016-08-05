#!/usr/bin/env/python

import sys
import os
import socket
import signal
import ReadingCommands
from Roomba import Roomba
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

global roomba

class SimpleHandler(WebSocket):

    def handleMessage(self):
        print("Message Received: " + str(self.data))

        # Shuts down the server and the Roomba proc
        if str(self.data) == "SHUTDOWN":
            print("Shutdown signal received, exiting...")
            roomba.term()
            self.close()
            sys.exit(0)
        
        # Moves the Roomba forward
        if str(self.data) == "START":
            print("Signalled to begin")
            self.sendMessage(unicode('VSTART'))
            roomba.forward()

        # Halts the Roomba movement to take reading
        if str(self.data) == "READING":
            print("Signalled to read, stopping movement")
            self.sendMessage(unicode('VREADING'))
            roomba.stop()
            print("Movement halted")

        # Signals the motor to spin the iPhone
        if str(self.data) == "READNOW":
            print("Taking reading...")
            self.sendMessage(unicode('VREADNOW'))
            ReadingCommands.spin()
            print("Done taking reading")
            roomba.forward()

        # Perform clean-up operations at end of experiment
        if str(self.data) == "ENDEXP":
            print("Signalled End of experiment")
            self.sendMessage(unicode('VENDEXP'))
            roomba.term()

    def handleConnected(self):
        print("New Connection: " + str(self.address))

    def handleClose(self):
        print("Closed Connection: " + str(self.address))

def signal_handler(signal, frame):
    print("TCP: SIGINT received, exiting...")
    roomba.term()
    sys.exit(0)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

if __name__ == '__main__':
    port = 9000
    ipaddr = get_ip_address()

    roomba = Roomba()

    server = SimpleWebSocketServer(str(ipaddr), port, SimpleHandler)
    server.serveforever()
    print("Serving TCP Socket on " + str(ipaddr) + ":" + str(port))

    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()

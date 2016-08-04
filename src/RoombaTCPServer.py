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

        if str(self.data) == "SHUTDOWN":
            print("Shutdown signal received, exiting...")
            self.close()
            sys.exit(0)

        if str(self.data) == "START":
            print("Signalled to begin")
            self.sendMessage(unicode('VSTART'))
            roomba.forward()

        if str(self.data) == "READING":
            print("Signalled to read, stopping movement")
            self.sendMessage(unicode('VREADING'))
            # STOP ROVER MOVEMENT
            roomba.stop()
            print("Movement halted")

        if str(self.data) == "READNOW":
            print("Taking reading...")
            self.sendMessage(unicode('VREADNOW'))
            ReadingCommands.spin()
            print("Done taking reading")
            roomba.forward()

        if str(self.data) == "ENDEXP":
            print("Signalled End of experiment")
            self.sendMessage(unicode('VENDEXP'))
            # RUN CLEAN UP SCRIPTS
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
    print("Serving TCP Socket on " + str(ipaddr) + ":" + str(port))

    server.serveforever()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()

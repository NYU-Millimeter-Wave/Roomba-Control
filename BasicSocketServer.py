#!/usr/bin/env/python

import signal
import sys
import os
import socket
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleHandler(WebSocket):

    def handleMessage(self):
        print("Message Received: " + str(self.data))
        if str(self.data) == "SHUTDOWN":
            print("Shutdown signal received, exiting...")
            self.close()
            sys.exit(0)
	if str(self.data)[:1] == "RUN":
            os.system(RoombaControl.py) 

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

#!/usr/bin/env/python

import signal
import sys
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleHandler(WebSocket):

    def handleMessage(self):
        print("Message Received: " + str(self.data))
        if str(self.data) == "SHUTDOWN":
            print("Shutdown signal received, exiting...")
            self.close()
            sys.exit(0)

    def handleConnected(self):
        print("New Connection: " + str(self.address))

    def handleClose(self):
        print("Closed Connection: " + str(self.address))

def signal_handler(signal, frame):
    print("SIGINT received, exiting...")
    server.close()
    sys.exit(0)

if __name__ == '__main__':
    server = SimpleWebSocketServer('127.0.0.1', 9000, SimpleHandler)
    signal.signal(signal.SIGINT, signal_handler)
    server.serveforever()
    signal.pause()

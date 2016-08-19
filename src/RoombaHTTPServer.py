#!/usr/bin/env/python

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import sys
import shutil
import mimetypes
import json
import signal
import socket

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class RoombaHTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        # Serve a GET request
        print("GET recieved")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Open the resultset and send it over
        with open("src/resultset.json", 'r') as resultset:
            jsonString = resultset.read()
            self.wfile.write(jsonString)

    def do_POST(self):
        """ Curl sample """
        """ curl -H "Content-Type: application/json" -X POST -d '{"username":"xyz","password":"abc"}' localhost:8000"""

        # Serve a POST request
        print("POST recieved")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Read from request and parse to json
        line = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        # Parse
        jsonString = line
        print(jsonString)

        # parsed_json = json.loads(jsonString)

        # Open resultset, truncate, rewrite
        with open("resultset.json", 'r+') as resultset:
            resultset.truncate()
            resultset.write(str(jsonString))

        return

runSignal = True

def get_ip_address():
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # return s.getsockname()[0]
    return '192.168.1.1'

def runWhileTrue(handler_class = RoombaHTTPServer,
        server_class = BaseHTTPServer.HTTPServer):
    # BaseHTTPServer.test(HandlerClass, ServerClass)
    server_addr = (get_ip_address(), 8000)
    htttpd = server_class(server_addr, handler_class)
    # htttpd.serve_forever()
    print("Serving HTTP on " + str(server_addr))
    while runSignal:
        htttpd.handle_request()

def signal_handler(signal, frame):
    print("HTTP: SIGINT received, exiting...")
    runSignal = False
    server_class.close()
    sys.exit(0)

if __name__ == '__main__':
    runWhileTrue()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()


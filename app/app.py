import http.server
import os
import socketserver
import time

APPNAME = os.environ["DNSDOCK_NAME"]
TARGET = os.environ["SERVER_TARGET"]

HOST = "dnsdock.docker"
PORT = 8000

def hit_target(target, port):
    conn = http.client.HTTPConnection("{:s}.{:s}:{:d}".format(target, HOST, port))
    conn.request("GET", "/")
    conn.close()

class PingPong(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(TARGET)
        self.send_response(200)
        time.sleep(3)
        hit_target(TARGET, PORT)

print("app {:s} with target {:s} running at {:s}.{:s}:{:d}".format(APPNAME, TARGET, APPNAME, HOST, PORT))

if APPNAME == "ping":
    time.sleep(3)
    hit_target(TARGET, PORT)

httpd = socketserver.TCPServer(("", PORT), PingPong)
httpd.serve_forever()

import sys
import socket
import datetime
import json

DATE_FORMAT = "%m:%d:%y:%H:%M:%S"

def send(key, value):
    sock = socket.socket()
    sock.connect(('localhost', 1234))
    payload = {
            "timestamp": datetime.datetime.now().strftime(DATE_FORMAT),
            "data": {
                key: value
                }
            }
    print "sending", json.dumps(payload)
    sock.send(json.dumps(payload));
    sock.close()

if __name__ == '__main__':
    send("cmd", sys.argv[1])

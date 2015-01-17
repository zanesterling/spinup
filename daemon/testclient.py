import sys
import socket
import json


def send(key, value):
    sock = socket.socket()
    sock.connect(('localhost', 1234))
    payload = {
        key: value
    }
    print "sending", json.dumps(payload)
    sock.send(json.dumps(payload));
    sock.close()

if __name__ == '__main__':
    send("cmd", sys.argv[1])
    send("other", "balH")

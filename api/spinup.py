import socket
import json

def send(key, value):
    sock = socket.socket()
    sock.connect(('localhost', 1234))
    payload = {
        key: value
    }
    sock.send(json.dumps(payload));
    sock.close()

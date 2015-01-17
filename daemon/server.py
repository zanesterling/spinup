import socket
import threading
import json
import time
import datetime

DATE_FORMAT = "%m:%d:%y:%H:%M:%S"
PORT = 1234

class Daemon(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('localhost', PORT))
        self.sock.listen(5)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cache = []
    
    def listen(self):
        def listen_thread():
            while True:
                conn, addr = self.sock.accept()
                data = conn.recv(4096)
                payload = {
                        "timestamp": datetime.datetime.now().strftime(DATE_FORMAT),
                        "data": json.loads(data)
                        }
                if len(self.cache) > 0 and self.cache[-1]["timestamp"] == payload["timestamp"] and \
                reduce(lambda a, b: a and b, [k1 != k2 for k1 in payload["data"].keys() for k2 in self.cache[-1]["data"].keys()]): # check that there is no intersection between the keys in the two payloads
                    print "merged"
                    for k in payload["data"]:
                        self.cache[-1]["data"][k] = payload["data"][k]
                else:
                    self.cache.append(payload)
                    print "appended"
                if 'cmd' in payload['data']:
                    if payload['data']['cmd'] == 'die':
                        break
                conn.close()
                print self.cache
                time.sleep(0.001)
        threading.Thread(group=None, target=listen_thread).start()


if __name__ == '__main__':
    daemon = Daemon()
    daemon.listen()

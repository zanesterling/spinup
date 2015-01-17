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
				# accept a connection
                conn, addr = self.sock.accept()

                # load data from socket
                data = conn.recv(4096)
                payload = {
                    "timestamp": datetime.datetime.now().strftime(DATE_FORMAT),
                    "data": json.loads(data)
                }

				# if the payload can be merged into the cache
                if shouldMergePayloads(payload):
                    # merge it
                    print "merged" #debug
                    for k in payload["data"].keys():
                        self.cache[-1]["data"][k] = payload["data"][k]
                else:
                    # append it to the cache
                    self.cache.append(payload)
                    print "appended" #debug

				# accept commands from sender
                if 'cmd' in payload['data']:
                    if payload['data']['cmd'] == 'die':
                        break

				# wrap up and prepare to sleep until the next cycle
                conn.close()
                print self.cache #debug
                time.sleep(0.001)

        def shouldMergePayloads(payload):
            # if there's nothing to merge with, return
            if len(self.cache) == 0:
                #print "cache empty"
                return False
            
            # if the payload and the cached payload have different timestamps, return
            lastInCache = self.cache[-1]
            if lastInCache["timestamp"] != payload["timestamp"]:
                #print "timestamps differ"
                return False
            
			# if there's any key overlap, return
            for k in payload["data"].keys():
                if k in lastInCache["data"].keys():
                    #print "keys overlap"
                    return False

            #print "all good"
            return True

        threading.Thread(group=None, target=listen_thread).start()

if __name__ == '__main__':
    daemon = Daemon()
    daemon.listen()

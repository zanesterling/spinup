import socket
import threading
import json
import time
import datetime
import urllib2

import performance

DATE_FORMAT = "%m:%d:%y:%H:%M:%S"
PORT = 1234
BASE_SLEEP_TIME = 1.0

class Daemon(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('localhost', PORT))
        self.sock.listen(5)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cache = []
    
    def listen(self):
        def listen_thread():
            while self.running:
				# accept a connection
                conn, addr = self.sock.accept()

                # load data from socket
                data = json.loads(conn.recv(4096))
                self.receive_msg(data)
				# accept commands from sender
                if 'cmd' in data:
                    if data['cmd'] == 'die':
                        self.running = False
                    elif data['cmd'] == 'send':
                        self.send()

				# wrap up and prepare to sleep until the next cycle
                conn.close()
                print self.cache #debug
                time.sleep(0.001)

        def cpu_polling_thread():
            while self.running:
                cpu = performance.get_CPU_usage()
                ram = performance.get_RAM_usage()
                self.receive_msg({
                    "cpu": cpu,
                    "ram": ram
                    })
                percent_to_sleep = 100 - max(cpu, ram)
                time.sleep((percent_to_sleep / 100.0) * BASE_SLEEP_TIME)


        self.running = True
        threading.Thread(group=None, target=listen_thread).start()
        threading.Thread(group=None, target=cpu_polling_thread).start()

    def receive_msg(self, data):
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

        payload = {
                "timestamp": datetime.datetime.now().strftime(DATE_FORMAT),
                "data": data
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

    def send(self, url="http://localhost:9001/"):
        req = urllib2.Request(url, json.dumps(self.cache), {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        self.cache = []

if __name__ == '__main__':
    daemon = Daemon()
    daemon.listen()

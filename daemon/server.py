import socket
import threading
import json

class Daemon(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('localhost', 1234))
        self.sock.listen(5)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def listen(self):
        def listen_thread():
            while True:
                conn, addr = self.sock.accept()
                data = conn.recv(4096)
                print data
                if data == 'die':
                    return
        threading.Thread(group=None, target=listen_thread).start()
        print "ok, it's inited"


if __name__ == '__main__':
    daemon = Daemon()
    daemon.listen()
    print "Done setting up daemon!"
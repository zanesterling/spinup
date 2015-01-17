import sys
import socket

if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('localhost', 1234))
    sock.send(sys.argv[1]);
    sock.close()

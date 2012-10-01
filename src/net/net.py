import asyncore
import os, socket, json

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
import led

class LEDConnection(asyncore.dispatcher_with_send):

    def __init__(self, conn, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.data = ''

    def handle_read(self):
        data = self.recv(8192)
        self.data += data
        led.tty.write(''.join(chr(g)+chr(r)+chr(b) for r,g,b in self.data) + chr(254))

class HTTPServer(asyncore.dispatcher):

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        LEDConnection(self, conn, addr)

s = HTTPServer(8002)
asyncore.loop()



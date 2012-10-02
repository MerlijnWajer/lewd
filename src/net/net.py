import asyncore
import os, socket, json

import sys, os
sys.path.append('..')
import led, transform

transform = transform.Transform(12, 10)

class LEDConnection(asyncore.dispatcher_with_send):

    def __init__(self, conn, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.data = ''

    def handle_read(self):
        data = self.recv(8192)
        self.data += data
        if len(self.data) <= 12*10*3:
            return

        screen.push_data(self.data[:12*10*3])
        self.data = self.data[(12*10*3):]

class SocketServer(asyncore.dispatcher):

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        LEDConnection(self, conn, addr)


screen = led.LedScreen()
s = SocketServer(8000)
asyncore.loop()



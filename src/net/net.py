import asyncore
import os, socket, json

import sys, os
sys.path.append('..')
import led, transform

transform = transform.Transform(12, 10)

from itertools import izip

from itertools import izip

class LEDConnection(asyncore.dispatcher_with_send):

    def __init__(self, conn, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.data = ''

    def handle_read(self):
        data = self.recv(8192)
        self.data += data
        if len(self.data) <= 12*10*3:
            return

        td = self.data[:12*10*3]
        #dat = ''.join(map(lambda (r, g, b): ''.join([g, r, b]), \
        #    izip(td[::2], td[1::2], td[2::2])))

        dat = zip(td[::3], td[1::3], td[2::3])

        i = 0
        for t in dat:
            r, g, b = map(ord, t)
            x, y = transform.translate(i)
            screen[x, y] = (r, g, b)

            i += 1

        screen.push()
        self.data = self.data[(12*10*3):]

class HTTPServer(asyncore.dispatcher):

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        LEDConnection(self, conn, addr)


screen = led.LedScreen()
s = HTTPServer(8000)
asyncore.loop()



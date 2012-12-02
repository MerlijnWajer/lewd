"""
  This file is part of the LEd Wall Daemon (lewd) project
  Copyright (c) 2009-2012 by ``brainsmoke'' and Merlijn Wajer (``Wizzup'')

    lewd is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lewd is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lewd.  If not, see <http://www.gnu.org/licenses/>.

  See the file COPYING, included in this distribution,
  for details about the copyright.
"""
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
        data = self.recv(12*10*3)
        self.data += data
        if len(self.data) < 12*10*3:
            return

        screen.push_data(self.data[:12*10*3])
        self.data = self.data[12*10*3:]

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



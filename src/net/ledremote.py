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
import sys, os
import socket
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
import abstractled

class RemoteLedScreen(abstractled.AbstractLed):
    def __init__(self, host, port, dim=(12,10)):
        """
Set Host and Port to where the net.py server is running.

Usage:

>>> screen = RemoteLedScreen('wallserver', 8000)
        """
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        abstractled.AbstractLed.__init__(self, dimension=dim)

        #self.sock = socket.create_connection((host, port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def push(self):
        """
Push the current frame contents to the screen.

>>> screen.push()
        """
        self.sock.send(''.join([chr(r)+chr(g)+chr(b) for (r,g,b) in self.buf]))

if __name__ == '__main__':
    screen = RemoteLedScreen('nosejs', 8000)

    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()

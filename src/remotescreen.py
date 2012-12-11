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
import sys, socket

import ledscreen

class RemoteScreen(ledscreen.BaseScreen):
    def __init__(self, dimension=(12,10), host, port):
        """
Set Host and Port to where the net.py server is running.

Usage:

>>> screen = RemoteLedScreen('wallserver', 8000)
        """
        ledscreen.BaseScreen.__init__(self, dimension=dimension)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def push(self):
        """
Push the current frame contents to the screen.

>>> screen.push()
        """
        self.sock.send(self.buf)

if __name__ == '__main__':
    screen = RemoteScreen()
    screen.load_frame( (x*20, y*24, (x+y)*11) for x in xrange(12) for y in xrange(10) )
    screen.push()


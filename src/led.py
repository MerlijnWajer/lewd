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
"""Low-level interface to the LED Wall at TechInc. http://techinc.nl"""

import sys, os, time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../lib/uspp'))

# Python serial communication module. Get it from pypi.
try:
    import uspp
except:
    print 'Error: USPP module missing!'
    # Do not stop, documentation parser doesn't require uspp.

from transform import Transform
import abstractled

__all__ = ['LedScreenException', 'LedScreen']

class LedScreenException(Exception):
    pass

class LedScreen(abstractled.AbstractLed):
    """
The low-level LED wall screen.
    """

    def __init__(self, fname='/dev/ttyACM0', brate=1000000, dim=(12,10), gamma=2.2):
        """
Initialise a LedScreen object.

>>> screen = LedScreen()
        """
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        abstractled.AbstractLed.__init__(self, dimension=dim, gamma=gamma)
        self.tty = uspp.SerialPort(fname, timeout=0)
        #self.tty = uspp.SerialPort(fname, speed=brate, timeout=0)
        os.environ['LEDWALL_TTY'] = fname
        os.system("stty -F $LEDWALL_TTY " + str(brate))

        self.transform = Transform(*dim)
        self.b = [(0,0,0)] * self.w * self.h

    def __setitem__(self, tup, val):
        abstractled.AbstractLed.__setitem__(self, tup, val)

        waiting = self.tty.inWaiting()
        if waiting > 0:
            _ = self.tty.read(waiting)

    def push(self):
        for x in xrange(self.w):
            for y in xrange(self.h):
                i = x + y * self.w
                self.b[self.transform.inverse( (x, y) )] = self.buf[i]

        self.tty.write( ''.join(chr(g)+chr(r)+chr(b) for r,g,b in self.b) + chr(254) )

if __name__ == '__main__':
    screen = LedScreen()

    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()


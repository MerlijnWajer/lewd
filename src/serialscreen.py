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

import ledscreen

class SerialScreen(ledscreen.LedScreen):
    """
The low-level LED wall screen.
    """
    def __init__(self, dimension=(12,10), gamma=2.2, devname='/dev/ttyACM0', baudrate=1000000):
        """
Initialise a SerialScreen object.

>>> screen = SerialScreen()
        """
        ledscreen.LedScreen.__init__(self, dimension, gamma)
        import uspp
        self.tty = uspp.SerialPort(fname, timeout=0)
        #self.tty = uspp.SerialPort(fname, speed=brate, timeout=0)
        os.environ['LEDWALL_TTY'] = fname
        os.system("stty -F $LEDWALL_TTY " + str(baudrate))

    def write_data(self, data):
        self.tty.write( data + chr(254) )

if __name__ == '__main__':
    screen = SPIScreen()
    screen.load_frame( (x*20, y*24, (x+y)*11) for x in xrange(12) for y in xrange(10) )
    screen.push()


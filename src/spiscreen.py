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

import time

import ledscreen

class SPIScreen(ledscreen.LedScreen):
    """
The low-level LED wall screen.
    """

    def __init__(self, dimensions=(12,10), gamma=2.2, devname='/dev/spidev0.0'):
        """
Initialise a SPIScreen object.

>>> screen = SPIScreen()
        """
        import spi
        ledscreen.LedScreen.__init__(self, dimension=dimensions, gamma=gamma)
        self.spi = spi.SPI(devname, 0, 1000000)

    def write_data(self, data):
        self.spi.transfer( str(data) )
        time.sleep(.001)

if __name__ == '__main__':
    screen = SPIScreen()
    screen.load_frame( (x*20, y*24, (x+y)*11) for x in xrange(12) for y in xrange(10) )
    screen.push()


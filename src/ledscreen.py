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

"""
BaseScreen implements basic buffer management + value/range checking.
Inherit this class to simplify your code. Eventually it would be nice if
vled, netled and led all used this module

"""

class BaseScreen(object):
    def __init__(self, dimension):
        """
        Initialise BaseScreen object. You need to do this in your class!
        Like this:
        >>> ledscreen.BaseScreen.__init__(self, dimension)
        """
        self.w, self.h = dimension

    def push(self):
        raise NotImplementedError('push not implemented')

    def load_data(self, data):
        self.buf = data
        assert len(self.buf) == 3 * self.w * self.h

    def load_frame(self, frame):
        """
Load three-dimensional array to framebuffer. Does not send anything yet.

>>> _ = (0,0,0)   # black
>>> X = (0,255,0) # green

>>> frame = [
...     [_,_,_,_,_,_,_,_,_,_,_,_,],
...     [_,_,_,X,_,_,_,_,_,X,_,_,],
...     [_,_,_,_,X,_,_,_,X,_,_,_,],
...     [_,_,_,X,X,X,X,X,X,X,_,_,],
...     [_,_,X,X,_,X,X,X,_,X,X,_,],
...     [_,X,X,X,X,X,X,X,X,X,X,X,],
...     [_,X,_,X,X,X,X,X,X,X,_,X,],
...     [_,X,_,X,_,_,_,_,_,X,_,X,],
...     [_,_,_,_,X,X,_,X,X,_,_,_,],
...     [_,_,_,_,_,_,_,_,_,_,_,_,],
... ],

>>> screen.load_frame(frame) # doesn't write yet
>>> screen.push()            # display
        """
        self.buf = ''.join( chr(c[0])+chr(c[1])+chr(c[2]) for row in frame for c in row )
        assert len(self.buf) == 3 * self.w * self.h

    def push_data(self, data):
        self.load_data(data)
        self.push()

    def push_frame(self, frame):
        self.load_frame(frame)
        self.push()

class LedScreen(BaseScreen):
    """
The low-level LED wall screen.
    """
    def __init__(self, dimension, gamma=2.2):
        """
        Initialise LedScreen object. You need to do this in your class!
        Like this:
        >>> ledscreen.BaseScreen.__init__(self, dimension)
        """
        BaseScreen.__init__(self, dimension)
        gamma = float(gamma)
        max_gamma = 255.**gamma
        self.gamma_map = [ chr(int( (1 + 2 * x**gamma / (max_gamma/255.)) //2 )) for x in xrange(256) ]
        for i, v in enumerate(self.gamma_map):
            if v == 254:
                self.gamma_map[i] = 253


    def ledindex(self, bitmapindex):
        """ Transform bitmapindex to ledindex """
        w, h = self.w, self.h
        x, y = bitmapindex % w, bitmapindex // w

        if x % 2 == 0:
            ind = h*(x+1)-1 - y
        else:
            ind = h*x + y
        return ind

    def push(self):
        data = bytearray(len(self.buf))
        gamma_map = self.gamma_map

        for i in xrange(0, len(data), 3):
            r, g, b = self.buf[i:i+3]

            j = self.ledindex(i//3)*3
            data[j  ] = gamma_map[ord(g)]
            data[j+1] = gamma_map[ord(r)]
            data[j+2] = gamma_map[ord(b)]

        self.write_data(data)


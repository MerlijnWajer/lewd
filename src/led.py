"""Low-level interface to the LED Wall at TechInc. http://techinc.nl"""

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../lib/uspp'))

# Python serial communication module. Get it from pypi.
try:
    import uspp
except:
    print 'Error: USPP module missing!'
    # Do not stop, documentation parser doesn't require uspp.

from transform import Transform

__all__ = ['LedScreenException', 'LedScreen']

class LedScreenException(Exception):
    pass

class LedScreen(object):
    """
The low-level LED wall screen.
    """

    def __init__(self, fname='/dev/ttyACM0', brate=115200, dim=(12,10), gamma=2.2):
        """
Initialise a LedScreen object.

>>> screen = LedScreen()
        """
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        self.tty = uspp.SerialPort(fname, speed=brate, timeout=0)
        self.w, self.h = dim
        self.buf = [(0, 0, 0)] * self.w * self.h
        self.transform = Transform(*dim)

        gamma = float(gamma)
        max_gamma = 255.**gamma
        self.gamma_map = [ int( (1 + 2 * x**gamma / (max_gamma/255.)) //2 ) for x in xrange(256) ]
        for i, v in enumerate(self.gamma_map):
            if v == 254:
                self.gamma_map[i] = 253

    def gamma_correct(self, colour):
        """
Returns gamma-corrected colour.
        """
        return tuple(self.gamma_map[c] for c in colour)

    def __setitem__(self, tup, val):
        """
Allows for easy frame access.
Use like:

>>> screen[(x, y)] = r, g, b
        """
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        if tup[0] not in range(0, self.w) or tup[1] not in range(0, self.h):
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        self.buf[self.transform.inverse(tup)] = self.gamma_correct(val)

        waiting = self.tty.inWaiting()
        if waiting > 0:
            _ = self.tty.read(waiting)

    def push(self):
        """
Push the current frame contents to the screen
        """
        self.tty.write( ''.join(chr(g)+chr(r)+chr(b) for r,g,b in self.buf) + chr(254) )

    def load_data(self, data):
        """
Load byte array to framebuffer. Does not send anything yet.
        """
        for i in xrange( min( len(data)/3, self.w*self.h ) ):
            x, y = i % self.w, i // self.w
            self[ (x, y) ] = tuple( ord(x) for x in data[i*3:(i+1)*3] )

    def push_data(self, data):
        """
Push byte array to the screen.
        """
        self.load_data(data)
        self.push()

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
        for y in xrange(max(len(frame), self.h)):
            for x in xrange(max(len(frame[y]), self.w)):
                self[ (x, y) ] = frame[y][x]

    def push_frame(self, frame):
        """
Push a three-dimensional array to the screen

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

>>> screen.push_frame(frame) # display invader
        """
        self.load_frame(frame)
        self.push()

if __name__ == '__main__':
    screen = LedScreen()

    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()


"""
AbstractLed implements basic buffer management + value/range checking.
Inherit this class to simplify your code. Eventually it would be nice if
vled, netled and led all used this module

"""


class AbstractLed(object):
    def __init__(self, dimension, gamma=2.2):
        """
        Initialise AbstractLed object. You need to do this in your class!
        Like this:
        >>> abstractled.AbstractLed.__init__(self, dimension)
        """
        self.w, self.h = dimension
        self.buf = [(0, 0, 0)] * self.w * self.h
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
        Default __setitem__, you should just use this. Or rather, you do not
        even need to implement this.

        Allows for easy frame access.
        Use like:

        >>> screen[(x, y)] = r, g, b
        """
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        x, y = tup

        if not 0 <= x < self.w and not 0 <= y < self.h:
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        i = x + y * self.w
        self.buf[i] = self.gamma_correct(val)

    def push(self):
        raise NotImplementedError('push not implemented')

    def load_data(self, data):
        """

        """
        l = max(len(data), len(self.buf))
        self.buf[:l] = data
        # TODO: Implement/test this
        raise NotImplementedError('load_data not implemented')

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

    def push_data(self, data):
        self.load_data(data)
        self.push()

    def push_frame(self, frame):
        self.load_frame(frame)
        self.push()


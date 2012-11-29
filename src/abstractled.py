"""
AbstractLed implements basic buffer management + value/range checking.
Inherit this class to simplify your code. Eventually it would be nice if
vled, netled and led all used this module

"""


class AbstractLed(object):
    def __init__(self, dimension):
        """
        Initialise AbstractLed object. You need to do this in your class!
        Like this:
        >>> abstractled.AbstractLed.__init__(self, dimension)
        """
        self.w, self.h = dimension
        self.buf = [(0, 0, 0)] * self.w * self.h

    def __setitem__(self, tup, val):
        """
        Default __setitem__, you should just use this. Or rather, you do not
        even need to implement this.
        """
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        x, y = tup

        if not 0 <= x < self.w and not 0 <= y < self.h:
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        i = x + y * self.w
        self.buf[i] = val

    def push(self):
        raise NotImplementedError('push not implemented')

    def load_data(self, data):
        """

        """
        l = max(len(data), len(self.buf))
        self.buf[:l] = data
        # TODO: Implement this
        raise NotImplementedError('load_data not implemented')

    def load_frame(self, frame):
        for y in xrange(max(len(frame), self.h)):
            for x in xrange(max(len(frame[y]), self.w)):
                self[ (x, y) ] = frame[y][x]

    def push_data(self, data):
        self.load_data(data)
        self.push()

    def push_frame(self, frame):
        self.load_frame(frame)
        self.push()


import random

class Munch:


    def __init__(self, w, h):
        self.w, self.h = w, h
        self.munch = [ [ [0,0,0] for x in xrange(w) ] for y in xrange(h) ]

        self.i = 0

    def next(self):
        munch = self.munch
        for j in xrange(self.i):
            for y in xrange(self.h):
                for x in xrange(self.w):
                    if y == (x ^ j):
                        munch[y][x][0] += 1
                        munch[y][x][0] %= 256
                        munch[y][x][1] += 5
                        munch[y][x][1] %= 256
                        munch[y][x][2] += 9
                        munch[y][x][2] %= 256

        if self.i == 16:
            self.i = 0
        self.i += 1
        return munch

animations = [ Munch ]

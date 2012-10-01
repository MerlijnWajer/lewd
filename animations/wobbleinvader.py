import random, cmath, math

def color(x, y, phase, opacity):

    phase *= 2 * math.pi

    rad, phi = cmath.polar(complex(x-5.5, y-4.5))

    phi /= 2.

    r, g = (math.sin( phi*2+phase*4 )+1.)/2., (math.sin(phi*2+phase)+1.)/2.

    b = (2. - r - g)/2.
    if b > 1.:
        b = 1.

    return int((r**4 * opacity)*255.), int((g**4 * opacity)*255.), int((b**4 * opacity)*255.)


class SpaceInvader(object):

    def __init__(self, w, h):
        self.c, self.p = -1, -1
        self.w, self.h = w, h

        _ = 0
        X = 1
    
        self.sprite= (
        [
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,X,_,_,_,_,_,X,_,_,],
            [_,_,_,_,X,_,_,_,X,_,_,_,],
            [_,_,_,X,X,X,X,X,X,X,_,_,],
            [_,_,X,X,_,X,X,X,_,X,X,_,],
            [_,X,X,X,X,X,X,X,X,X,X,X,],
            [_,X,_,X,X,X,X,X,X,X,_,X,],
            [_,X,_,X,_,_,_,_,_,X,_,X,],
            [_,_,_,_,X,X,_,X,X,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
        ],
        [
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,X,_,_,_,_,_,X,_,_,],
            [_,X,_,_,X,_,_,_,X,_,_,X,],
            [_,X,_,X,X,X,X,X,X,X,_,X,],
            [_,X,X,X,_,X,X,X,_,X,X,X,],
            [_,X,X,X,X,X,X,X,X,X,X,X,],
            [_,_,X,X,X,X,X,X,X,X,X,_,],
            [_,_,_,X,_,_,_,_,_,X,_,_,],
            [_,_,X,_,_,_,_,_,_,_,X,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
        ])

    def next(self):
        self.c += 1
        self.c %= len(self.sprite*5)
        self.p += 1
        self.p %= 512
        phase = self.p/512.
        return [ [ color(x, y, phase, self.sprite[int(self.c/5)][y][x]) for x in xrange(self.w) ] for y in xrange(self.h) ]

animations = [ SpaceInvader ]

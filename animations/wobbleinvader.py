import random, cmath, math

def color(x, y, phase, opacity):

    phase *= 2 * math.pi

    rad, phi = cmath.polar(complex(x-6, y-4))

    r, g, b = (math.cos(-rad*.5+phase)+1.)/2, (math.cos(-rad*.5+phase+2/3.*math.pi)+1.)/2, (math.cos(-rad*.5+phase+4/3.*math.pi)+1.)/2

    return int(r**2 *255*opacity),int(g**2 *255*opacity),int(b**2 *255*opacity)



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
        self.c %= len(self.sprite*25)
        self.p += 1
        self.p %= 64
        phase = self.p/64.
        return [ [ color(x, y, phase, self.sprite[int(self.c/25)][y][x]) for x in xrange(self.w) ] for y in xrange(self.h) ]

animations = [ SpaceInvader ]

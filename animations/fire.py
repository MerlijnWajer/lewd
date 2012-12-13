import random

class Fire:

    def __init__(self, w, h):
        self.old = [ [ 0 ] * w*2 for y in xrange(h*2+2) ]
        self.new = [ [ 0 ] * w*2 for y in xrange(h*2+2) ]
        self.w, self.h = w*2, h*2 
        self.mapping = [ min( int((x/256.)**1.25 / 3.7 * 256.), 2047) for x in xrange(2048) ]
        self.colortab = [ self.color(x/256.) for x in xrange(256) ] + [(0,0,0)]*2048

    def color(self, x):
        r,g,b = (x**1*3, x**1.5*4., x**2)
        if r > 1.:
            r = 1.
        if g > 1.:
            g = 1.
        if b > 1.:
            b = 1.
        if (r, g, b) == (1., 1., 1.):
            r,g,b = 0.,0.,0.
        return int(r*255),int(g*255),int(b*255)

    def next(self):
        w, h = self.w, self.h

        self.old, self.new = self.new, self.old
        
        for y in xrange(h+1):
            if y == h:
                r = random.getrandbits(w)
            for x in xrange(w):
                s = 0
                if y == h:
                    s += 650 * (r&1)
                    r >>= 1
                else:
                    for dx in (-1, 0, 1):
                        if 0 <= x+dx < w:
                            s += self.old[y+1][x+dx]
                self.new[y][x] = self.mapping[min(s,2047)]
            print

        img = self.new
        return [ [ self.colortab[ (img[y*2][x*2]+img[y*2][x*2+1]+img[y*2+1][x*2]+img[y*2+1][x*2+1])/4 ] for x in xrange(self.w/2) ] for y in xrange(self.h/2) ]

animations = [ Fire ]

import cmath, math

def color(phase):

    phase *= 2 * math.pi / 4096. / 2

    r, g, b = (math.cos(phase)+1.)/2, (math.cos(phase+2/3.*math.pi)+1.)/2, (math.cos(phase+4/3.*math.pi)+1.)/2

    return int(r*255),int(g*255),int(b*255)

class Plasma(object):

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.n_phases = 64
        self.p = 0
        self.frame = [ [ (0,0,0) for x in xrange(w) ] for y in xrange(h) ]
        self.sintab = [ int(math.sin((x*math.pi*2.)/512)*1024) for x in xrange(512) ] # tradition

        self.p = (0,0,0,0)

    def next(self):
        p1, p2, p3, p4 = self.p
        
        d3, d4 = p3, p4

        for y in xrange(self.h):
            d1, d2 = p1+50, p2+30
            d3 &= 0x1ff
            d4 &= 0x1ff
            for x in xrange(self.w):
                d1 &= 0x1ff
                d2 &= 0x1ff
                v = self.sintab[d1] + self.sintab[d2] + self.sintab[d3] + self.sintab[d4]
                self.frame[y][x] = color(v)
                d1, d2 = d1+50, d2+30
            d3, d4 = d3+30, d4+10
        p1 += 9
        p3 += 8

        self.p = p1, p2, p3, p4

        return self.frame

animations = [ Plasma ]

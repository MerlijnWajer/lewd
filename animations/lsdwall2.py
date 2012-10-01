import cmath, math

def color(x, y, phase):

    phase *= 2 * math.pi

    rad, phi = cmath.polar(complex(x-5.5, y-4.5))

    r, g, b = (math.cos(-rad*.5-phase*4)+1.)/2, (math.cos(-rad*.5+phase+2/3.*math.pi)+1.)/2, (math.cos(-rad*.5+phase+4/3.*math.pi)+1.)/2

    return int(r**2 *255),int(g**2 *255),int(b**2 *255)

class Wobble(object):

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.n_phases = 512
        self.p = 0

    def next(self):
        
        phase = float(self.p)/self.n_phases

        frame = [ [ color(x, y, phase) for x in xrange(self.w) ] for y in xrange(self.h) ]
        self.p += 1
        self.p %= self.n_phases

        return frame

animations = [ Wobble ]

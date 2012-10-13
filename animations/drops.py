import numpy as np
import random as rd
import scipy.ndimage as nd

treshold = 1.
circleupdatefreq = 0.8
updatefreq = 0.11
colors = [  [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255] ]

class Drops(object):

    def addDrops(self):
        # do blending
        self.grid = self.basisgrid.copy()
        for w in xrange(self.w):
            for h in xrange(self.h):
                for drop in self.drops:
                    y, x, a, color = drop
                    distance = ((w - y)**2 + (h - x)**2)**0.5
                    if (abs(distance - a) < treshold):
                        self.grid[h][w] = self.grid[h][w] + color

        for i in xrange(3): 
            self.grid[:, :, i] = nd.gaussian_filter(self.grid[:,:,i], 1, 0, mode = 'nearest')

        self.grid *= 2.5
        
        # update drops
        for i in xrange(len(self.drops)):
            self.drops[i] = (self.drops[i][0], self.drops[i][1], \
                    self.drops[i][2] + circleupdatefreq, self.drops[i][3])

        # delete drops
        self.drops = [ drop for drop in self.drops if drop[2] < \
                        ((self.w)**2 + (self.h)**2)**0.5 ] 
            
        # add new drop
        if rd.random() < updatefreq:
            self.drops.append((rd.randrange(0, self.w), rd.randrange(0, self.h), \
                            0, colors[rd.randrange(0, len(colors))]))
        return

    def __init__(self, w, h):
        self.w, self.h = w*2, h*2
        self.background = [0, 0, 0]
        self.basisgrid = np.ones((self.h, self.w, 3))
        self.grid = np.ones((self.h, self.w, 3))
        self.basisgrid = self.basisgrid[::] * self.background
        self.drops = []

    def next(self):
        self.addDrops()
		
        scaled = nd.interpolation.zoom(self.grid, (.5, .5, 1))
        return [ [ map(int, tuple(map(lambda x: min(x, 255), scaled[y][x])))\
                    for x in xrange(self.w/2) ] for y in xrange(self.h/2) ]

animations = [ Drops ]

import random, time

def get_random_bitmap(w, h):
    return [ [ random.randint(0,1) for x in xrange(w) ] for y in xrange(h) ]

def game_of_life(prev):
    w, h = len(prev[0]), len(prev)
    new = [ [ 0 for x in xrange(w) ] for y in xrange(h) ]
    for y in xrange(h):
        for x in xrange(w):
            n = 0
            for dx, dy in ( (-1, -1), (-1, 0), (-1, 1),
                            ( 0, -1),          ( 0, 1),
                            ( 1, -1), ( 1, 0), ( 1, 1) ):
                if prev[(y+dy)%h][(x+dx)%w]:
                    n += 1
            if n == 3:
                new[y][x] = 1
            elif n == 2 and prev[y][x]:
                new[y][x] = 1

    return new

class FadeGameOfLife(object):

    def __init__(self, w, h, phase):
        self.cells_next = get_random_bitmap(w, h)
        self.phase = phase-1
        self.max_phase = phase
        self.w, self.h = w, h
        self.timeout = 64

    def next(self):
        w, h = self.w, self.h
        self.phase += 1
        if self.phase == self.max_phase:
            self.phase = 0
            self.cells_prev, self.cells_next = self.cells_next, game_of_life(self.cells_next)
            self.timeout -= 1
            if self.cells_prev == self.cells_next or self.timeout == 0:
                self.cells_next = get_random_bitmap(w, h)
                self.timeout = 64

        counterphase = (self.max_phase-self.phase)
        return [ [ int( (self.cells_prev[y][x]*counterphase + 
                         self.cells_next[y][x]*self.phase) *255. / self.max_phase ) for x in xrange(w) ]
                                                                                    for y in xrange(h) ]

class GameOfThreeLives(object):

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.red_game = FadeGameOfLife(w, h, 20)
        self.green_game = FadeGameOfLife(w, h, 10)
        self.blue_game = FadeGameOfLife(w, h, 30)

    def next(self):
        red = self.red_game.next()
        green = self.green_game.next()
        blue = self.blue_game.next()

        return [ [ [red[y][x], green[y][x], blue[y][x]] for x in xrange(self.w) ]
                                                        for y in xrange(self.h) ]

animations = [ GameOfThreeLives ]

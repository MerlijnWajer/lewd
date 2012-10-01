
class SpaceInvader(object):

    def __init__(self, w, h):
        self.cur = 0

        _ = (0,0,0)
        X = (0,255,0)
    
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
        frame = self.sprite[self.cur//20]
        self.cur += 1
        self.cur %= len(self.sprite)*20
        return frame

animations = [ SpaceInvader ]

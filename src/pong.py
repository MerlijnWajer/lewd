import sync
import curses
import sys

import ext

keyevents = ext.input.CursesInput()

sys.path.append('..')

use_socket = False
for arg in sys.argv[1:]:
    if arg == '-net':
        use_socket = True

if use_socket:
    sys.path.append('net')
    import ledremote
    s = ledremote.RemoteLedScreen('ledwall', 8000)
else:
    import led
    s = led.LedScreen()

WHITE, BLACK, GREY = (255,255,255), (0,0,0), (63,63,63)
X, _ = WHITE, BLACK

numbers = [
    [
        [X,X,X,X],
        [X,_,_,X],
        [X,_,X,X],
        [X,X,_,X],
        [X,_,_,X],
        [X,_,_,X],
        [X,X,X,X],
    ], [
        [_,X,X,_],
        [_,_,X,_],
        [_,_,X,_],
        [_,_,X,_],
        [_,_,X,_],
        [_,_,X,_],
        [_,_,X,_],
    ], [
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [X,X,X,X],
        [X,_,_,_],
        [X,_,_,_],
        [X,X,X,X],
    ], [
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [X,X,X,X],
    ], [
        [X,_,_,X],
        [X,_,_,X],
        [X,_,_,X],
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [_,_,_,X],
    ], [
        [X,X,X,X],
        [X,_,_,_],
        [X,_,_,_],
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [X,X,X,X],
    ], [
        [X,X,X,X],
        [X,_,_,_],
        [X,_,_,_],
        [X,X,X,X],
        [X,_,_,X],
        [X,_,_,X],
        [X,X,X,X],
    ], [
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [_,_,_,X],
        [_,_,_,X],
        [_,_,_,X],
        [_,_,_,X],
    ], [
        [X,X,X,X],
        [X,_,_,X],
        [X,_,_,X],
        [X,X,X,X],
        [X,_,_,X],
        [X,_,_,X],
        [X,X,X,X],
    ], [
        [X,X,X,X],
        [X,_,_,X],
        [X,_,_,X],
        [X,X,X,X],
        [_,_,_,X],
        [_,_,_,X],
        [X,X,X,X],
    ],
]

gameover = [
        [
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [X,_,X,_,X,_,X,_,X,_,_,X,],
            [X,_,X,_,X,_,X,_,X,X,_,X,],
            [X,_,X,_,X,_,X,_,X,_,X,X,],
            [_,X,_,X,_,_,X,_,X,_,X,X,],
            [_,X,_,X,_,_,X,_,X,_,_,X,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
        ], [
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [X,_,_,X,_,_,_,X,X,_,X,X,],
            [X,_,X,_,X,_,X,_,_,_,X,_,],
            [X,_,X,_,X,_,X,X,X,_,X,X,],
            [X,_,X,_,X,_,_,_,X,_,X,_,],
            [X,X,_,X,_,_,X,X,_,_,X,X,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
            [_,_,_,_,_,_,_,_,_,_,_,_,],
        ],
]

playerup = True
computerup = True
x, y = (10, 5)
dx, dy = (1, 1)
w, h = 20, 20

PLAYER, COMPUTER = 0, 1
TOP, HEIGHT, DIRECTION = 0, 1, 2
pads = [ [4, 7, 1], [4, 7, 1] ]

fps = 25.
metronome = sync.Metronome(fps)
metronome.start()

empty_frame = [ [BLACK] * 12 for j in xrange(10) ]

trail = []

score = [0,0]

def blend(frame1, frame2, d):
    return [ [ [ int(frame2[y][x][c]*d - frame1[y][x][c]*(d-1.))
                 for c in xrange(3)  ]
                 for x in xrange(12) ]
                 for y in range(10)  ]


def draw_pads(frame):
    xcoords = [0, 11]
    for i in range(len(pads)):
        ymin, ymax = pads[i][TOP], pads[i][TOP]+pads[COMPUTER][HEIGHT]
        if ymin % 2 == 1:
            frame[ymin/2][xcoords[i]] = GREY
            ymin += 1
        if ymax % 2 == 1:
            frame[ymax/2][xcoords[i]] = GREY
            ymax -= 1
        for y in xrange(ymin/2, ymax/2):
            frame[y][xcoords[i]] = WHITE

def draw_ball(frame):
    global trail
    trail = [ (x, y) ] + trail[:3]
    for i, (tx, ty) in enumerate(trail):
        frame[int(ty/2)][1+int(tx/2)] = (63+64*i, 63+64*i, 63+64*i)

def draw_score(frame, score):
    for i, n in enumerate(score):
        for y in range(len(numbers[n])):
            for x in range(len(numbers[n][y])):
                frame[1+y][i*8+x] = numbers[n][y][x]
    frame[4][5] = frame[4][6] = WHITE

try:
    while True:
        f = keyevents.poll()

        if f == 'q':
            break

        elif f == 'w':
            pads[PLAYER][DIRECTION] = -1
        elif f == 's':
            pads[PLAYER][DIRECTION] = 1

        # AI against AI hack :-P
        if y < pads[PLAYER][TOP]+pads[COMPUTER][HEIGHT]/2.:
            pads[PLAYER][DIRECTION] = -1
        elif y > pads[PLAYER][TOP]+pads[COMPUTER][HEIGHT]/2.:
            pads[PLAYER][DIRECTION] = 1


        if not 0 <= y+dy < 20:
            dy = -dy

        x, y = x+dx, y+dy

        for i in range(len(pads)):
            if 0 <= pads[i][TOP]+pads[i][DIRECTION] and \
                    pads[i][TOP]+pads[i][DIRECTION]+pads[COMPUTER][HEIGHT] <= 20:
                 pads[i][TOP] += pads[i][DIRECTION]

        if y < pads[COMPUTER][TOP]+pads[COMPUTER][HEIGHT]/2.:
            pads[COMPUTER][DIRECTION] = -1
        elif y > pads[COMPUTER][TOP]+pads[COMPUTER][HEIGHT]/2.:
            pads[COMPUTER][DIRECTION] = 1

        if not 0 <= y+dy < 20:
            dy = -dy

        if x+dx < 0 and pads[0][TOP] <= y < pads[0][TOP]+pads[0][HEIGHT]:
            dx = -dx
            dy = (y - (pads[0][TOP]+pads[0][HEIGHT]/2.) )/2.

        if x+dx >= w and pads[1][TOP] <= y < pads[1][TOP]+pads[1][HEIGHT]:
            dx = -dx
            dy = (y - (pads[1][TOP]+pads[1][HEIGHT]/2.) )/2.
        
        if not 0 <= x+dx < 20:
            x, y = (10, 5)
            trail = []
            score[int(dx < 0)] += 1
            if score[int(dx < 0)] > 9:
                score = [0,0]
                for i in ( range(20)+range(20, 0, -1) )*4:
                    s.push_frame(blend(empty_frame, gameover[int(dx < 0)], i/20.))
                    metronome.sync()

            frame = [ [BLACK] * 12 for j in xrange(10) ]
            score_frame = [ [BLACK] * 12 for j in xrange(10) ]
            draw_score(score_frame, score)
            draw_pads(frame)
            for i in range(50):
                s.push_frame(blend(score_frame, frame, i/50.))
                metronome.sync()
            dx, dy = -dx, 1

        frame = [ [(0,0,0)] * 12 for i in xrange(10) ]
        draw_pads(frame)
        draw_ball(frame)
        s.push_frame(frame)

        metronome.sync()

finally:
    pass
    curses.reset_shell_mode()


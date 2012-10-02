import sync
import curses
import sys

sys.path.append('..')
sys.path.append('net')
import ledremote


import animations
animations = [ x(12, 10) for x in animations.animations ]

s = ledremote.RemoteLedScreen()

window = curses.initscr()
curses.raw()
curses.noecho()
window.nodelay(True)

def getkey():
    f = window.getch()
    if f == -1:
        return None
    else:
        return chr(f)

metronome = sync.Metronome(fps=25.)
metronome.start()


current = 0

try:
    while True:

        f = getkey()

        if f == 'q':
            break

        elif f == ',':
            current -=1;
        elif f == '.':
            current +=1;

        current %= len(animations)

        s.push_frame(animations[current].next())

        metronome.sync()

finally:
    pass
    curses.reset_shell_mode()


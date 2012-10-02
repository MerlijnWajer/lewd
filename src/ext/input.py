import curses

class CursesInput():
    def __init__(self):
        self.window = curses.initscr()
        curses.raw()
        curses.noecho()
        self.window.nodelay(True)

    def __del__(self):
        curses.reset_shell_mode()

    def poll(self):
        f = self.window.getch()
        if f == -1:
            return None
        if f in range(0, 255):
            return chr(f)
        return None


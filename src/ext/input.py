"""
  This file is part of the LEd Wall Daemon (lewd) project
  Copyright (c) 2009-2012 by ``brainsmoke'' and Merlijn Wajer (``Wizzup'')

    lewd is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lewd is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lewd.  If not, see <http://www.gnu.org/licenses/>.

  See the file COPYING, included in this distribution,
  for details about the copyright.
"""
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


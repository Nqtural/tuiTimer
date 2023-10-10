import curses
import time
from pynput import keyboard
from chart import get_chart
from timer import timer
from db import Database
import threading
import re


scramble_alg = None


def replace_color_codes(input_string):
    color_pattern = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return re.sub(color_pattern, '', input_string)


def chart(mainwin, args):
    height, width = mainwin.getmaxyx()
    graph = replace_color_codes(get_chart(
        [float(solve[1]) for solve in args["database"].read()],
        height-1,
        width-1))
    mainwin.addstr(
        0 if len(graph) > 21 else int((height - 1) / 2),
        0 if len(graph) > 21 else int((width - 21) / 2),
        graph)
    mainwin.refresh()


def algorithms(mainwin, args):
    pass


class Tab:
    def __init__(self, name, function, index):
        self.name = name
        self.function = function
        self.index = index


class Tabs:
    tabs = {
        "timer": Tab("Timer", timer, 0),
        "chart": Tab("Chart", chart, 1),
        "algorithms": Tab("Algorithms", algorithms, 2)
    }

    def __init__(self, win, color, color_active):
        self.win = win
        self.height, self.width = self.win.getmaxyx()
        self.color = color
        self.color_active = color_active

    def draw(self, active):
        for key, tab in self.tabs.items():
            self.win.addstr(
                0,
                int(tab.index * self.width / 3) +
                int(((self.width / 3) - len(tab.name)) / 2),
                tab.name,
                self.color_active if key == active else self.color
            )
        self.win.refresh()

    def switch_to(self, tab, mainwin, args={}):
        mainwin.clear()
        mainwin.refresh()
        self.draw(tab)
        self.tabs[tab].function(mainwin, args)


def main(stdscr):
    from db import Database
    database = Database()
    database.new_session()

    stdscr.refresh()

    # Tab
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # Tab active
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

    height, width = stdscr.getmaxyx()

    tabs = Tabs(curses.newwin(1, width, 0, 0), curses.color_pair(1), curses.color_pair(2))

    mainwin = curses.newwin(height - 1, width, 1, 0)

    mainwin.refresh()
    tabs.switch_to("timer", mainwin, args={
        "cover": False,
        "decimals": 3,
        "database": database
    })
    while 1:
        key = stdscr.getch()
        if key == curses.KEY_F1:
            tabs.switch_to("timer", mainwin, args={
                "cover": False,
                "decimals": 3,
                "database": database
            })
        elif key == curses.KEY_F2:
            tabs.switch_to("chart", mainwin, args={
                "database": database
            })
        elif key == curses.KEY_F3:
            tabs.switch_to("algorithms", mainwin)
        elif key == ord('q'):
            return


curses.wrapper(main)
curses.endwin()

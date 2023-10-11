import curses
import time
import threading
import re
from pynput import keyboard
from chart import get_chart
from timer import timer
from algorithms import algorithms_map
from db import Database


scramble_alg = None
stop_algorithm_listener = False
stop_solve_listener = False
toggle_plustwo_bool = False
delete_active_solve = False
delete_solve_confirmed = False
active_solve = 0
algorithm_page = ["OLL", "Awkward Shape"]
last_oll_page = "Awkward Shape"
last_pll_page = "Adjacent Corner Swap"


def replace_color_codes(input_string):
    color_pattern = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return re.sub(color_pattern, '', input_string)


def chart(mainwin, args):
    height, width = mainwin.getmaxyx()
    graph = replace_color_codes(get_chart(
        [float(solve[2]) for solve in args["database"].read()],
        height-1,
        width-1))
    mainwin.addstr(
        0 if len(graph) > 21 else int((height - 1) / 2),
        0 if len(graph) > 21 else int((width - 21) / 2),
        graph)
    mainwin.refresh()


def get_algorithm_positions(height, width):
    # 3x3
    # if int(width / 3) > 67:
    return [
        (int(height / 4) - 3, 0),
        (int(height / 4) - 3, int(width / 3)),
        (int(height / 4) - 3, int(width * 2 / 3)),
        (int(height * 2 / 4) - 3, 0),
        (int(height * 2 / 4) - 3, int(width / 3)),
        (int(height * 2 / 4) - 3, int(width * 2 / 3)),
        (int(height * 3 / 4) - 3, 0),
        (int(height * 3 / 4) - 3, int(width / 3)),
        (int(height * 3 / 4) - 3, int(width * 2 / 3))
    ]
    # 2x4
    # else:
    #    return [
    #         (int(height / 5) - 3, 0),
    #         (int(height / 5) - 3, int(width / 2)),
    #         (int(height * 2 / 5) - 3, 0),
    #         (int(height * 2 / 5) - 3, int(width / 2)),
    #         (int(height * 3 / 5) - 3, 0),
    #         (int(height * 3 / 5) - 3, int(width / 2)),
    #         (int(height * 4 / 5) - 3, 0),
    #         (int(height * 4 / 5) - 3, int(width / 2)),
    #     ]


def replace_icon(icon):
    string = icon[0].replace("v", "▄▄").replace(">", " █").replace("f", "██").replace("<", "█ ").replace("^", "▀▀")
    # string = icon[0].replace("v", "▒▒").replace(">", "▒▒").replace("f", "██").replace("<", "▒▒").replace("^", "▒▒")
    color = curses.color_pair(1)
    if icon[1] == "b": 
        color = curses.color_pair(6)
    elif icon[1] == "y":
        color = curses.color_pair(7)
    elif icon[1] == "g":
        color = curses.color_pair(8)
    elif icon[1] == "B":
        color = curses.color_pair(9)
    elif icon[1] == "o":
        color = curses.color_pair(10)
    elif icon[1] == "r":
        color = curses.color_pair(11)

    return (string, color)


def print_icon(mainwin, y, x, icon):
    for i in range(0, int(len(icon) / 2)):
        mainwin.addstr(y, x + (i * 2), *replace_icon(icon[i * 2:(i + 1) * 2]))


def print_algorithm(mainwin, y, x, name, icon, algorithm):
    # Line 1:
    print_icon(mainwin, y, x, icon[0])
    # Line 2:
    print_icon(mainwin, y + 1, x, icon[1])
    mainwin.addstr(y + 1, x + 12, name + ":")
    # Line 3:
    print_icon(mainwin, y + 2, x, icon[2])
    # Line 4:
    print_icon(mainwin, y + 3, x, icon[3])
    mainwin.addstr(y + 3, x + 12, algorithm)
    # Line 5:
    print_icon(mainwin, y + 4, x, icon[4])


def switch_algorithm_page(key):
    global algorithm_page
    if key == keyboard.Key.space or key == keyboard.Key.down or key == keyboard.Key.up:
        last_page = algorithm_page[1]
        global last_pll_page
        global last_oll_page
        if algorithm_page[0] == "OLL":
            algorithm_page = ["PLL", last_pll_page]
            last_oll_page = last_page
        else:
            algorithm_page = ["OLL", last_oll_page]
            last_pll_page = last_page
        return False
    elif key == keyboard.Key.right:
        try:
            algorithm_page = [algorithm_page[0], list(algorithms_map[algorithm_page[0]].keys())[list(algorithms_map[algorithm_page[0]].keys()).index(algorithm_page[1]) + 1]]
        except IndexError:
            algorithm_page = [algorithm_page[0], list(algorithms_map[algorithm_page[0]].keys())[0]]
        return False
    elif key == keyboard.Key.left:
        algorithm_page = [algorithm_page[0], list(algorithms_map[algorithm_page[0]].keys())[list(algorithms_map[algorithm_page[0]].keys()).index(algorithm_page[1]) - 1]]
        return False
    elif key == keyboard.Key.f1 or key == keyboard.Key.f2 or key == keyboard.Key.f3:
        global stop_algorithm_listener
        stop_algorithm_listener = True
        return False


def algorithms(mainwin, args):
    global stop_algorithm_listener
    global algorithm_page
    global stop_algorithm_listener
    stop_algorithm_listener = False
    while True:
        mainwin.clear()
        title = f"{algorithm_page[0]}: {algorithm_page[1]}"
        width = mainwin.getmaxyx()[1]
        mainwin.addstr(2, int((width - len(title)) / 2), title)
        for i, item in enumerate(algorithms_map[algorithm_page[0]][algorithm_page[1]].items()):
            print_algorithm(mainwin, *args["algorithm_positions"][i], item[0], item[1]["icon"], item[1]["algorithm"])
        mainwin.refresh()
        with keyboard.Listener(
            on_press=switch_algorithm_page) as listener:
            listener.join()
        
        if stop_algorithm_listener: break


def solve_keybinds(key):
    global active_solve
    try:
        if key.char == "+":
            global toggle_plustwo_bool
            toggle_plustwo_bool = True
            return False
        elif key.char == "j":
            active_solve += 1
            return False
        elif key.char == "k":
            active_solve += -1
            return False
    except AttributeError:
        if key == keyboard.Key.f1 or key == keyboard.Key.f3 or key == keyboard.Key.f4:
            global stop_solve_listener
            stop_solve_listener = True
            return False
        elif key == keyboard.Key.down:
            active_solve += 1
            return False
        elif key == keyboard.Key.up:
            active_solve += -1
            return False
        elif key == keyboard.Key.delete or key == keyboard.Key.backspace:
            global delete_active_solve
            delete_active_solve = True
            return False


def confirm_deletion(key):
    try:
        if key.char.lower() == "y":
            global delete_solve_confirmed
            delete_solve_confirmed = True
        return False
    except AttributeError:
        if key == keyboard.Key.esc:
            return False


def solves(mainwin, args):
    height, width = mainwin.getmaxyx()
    x = [int(width / 4) * i for i in range(0, 3)] + [width]
    global stop_solve_listener
    global active_solve
    stop_solve_listener = False
    while True:
        mainwin.clear()
        solves = args["database"].read(last=-1)
        if active_solve == -1:
            active_solve = len(solves) - 1
        elif active_solve >= len(solves):
            active_solve = 0
        mainwin.addstr(1, x[0], "Date", curses.A_BOLD)
        mainwin.addstr(1, x[1], "Time", curses.A_BOLD)
        mainwin.addstr(1, x[2], "+2", curses.A_BOLD)
        mainwin.addstr(1, x[3] - len("Scramble"), "Scramble", curses.A_BOLD)
        for i, solve in enumerate(solves[::-1]):
            if i == active_solve:
                mainwin.addstr(i + 2, 0, " " * width, curses.color_pair(5))
                active_id = solve[0]
            mainwin.addstr(
                i + 2, x[0], str(solve[1]),
                curses.color_pair(5) | curses.A_BOLD if i == active_solve else curses.color_pair(1))
            mainwin.addstr(
                i + 2, x[1], f"{solve[2]:.3f}",
                curses.color_pair(5) | curses.A_BOLD if i == active_solve else curses.color_pair(1))
            mainwin.addstr(
                i + 2, x[2], "Yes" if solve[4] else "No",
                curses.color_pair(5) | curses.A_BOLD if i == active_solve else curses.color_pair(1))
            mainwin.addstr(
                i + 2, x[3] - len(solve[3]), solve[3],
                curses.color_pair(5) | curses.A_BOLD if i == active_solve else curses.color_pair(1))
        mainwin.refresh()
        with keyboard.Listener(
            on_press=solve_keybinds) as listener:
            listener.join()

        if stop_solve_listener: break

        global toggle_plustwo_bool
        if toggle_plustwo_bool:
            try:
                args["database"].toggle_plustwo(active_id)
            except UnboundLocalError: pass # There are no solves in current session
            toggle_plustwo_bool = False

        global delete_active_solve
        if delete_active_solve and solves:
            mainwin.addstr(height - 1, 0, "Press 'y' to confirm deletion: ")
            mainwin.refresh()
            curses.curs_set(1)
            with keyboard.Listener(
                on_press=confirm_deletion) as listener:
                listener.join()
            global delete_solve_confirmed
            if delete_solve_confirmed:
                args["database"].delete(active_id)
                delete_solve_confirmed = False
            curses.curs_set(0)
            delete_active_solve = False


class Tab:
    def __init__(self, name, function, index):
        self.name = name
        self.function = function
        self.index = index


class Tabs:
    tabs = {
        "timer": Tab("Timer", timer, 0),
        "solves": Tab("Solves", solves, 1),
        "chart": Tab("Chart", chart, 2),
        "algorithms": Tab("Algorithms", algorithms, 3)}

    def __init__(self, win, color, color_active):
        self.win = win
        self.height, self.width = self.win.getmaxyx()
        self.color = color
        self.color_active = color_active

    def draw(self, active):
        for key, tab in self.tabs.items():
            self.win.addstr(
                0,
                int(tab.index * self.width / 4) +
                int(((self.width / 4) - len(tab.name)) / 2),
                tab.name,
                self.color_active if key == active else self.color)
        self.win.refresh()

    def switch_to(self, tab, mainwin, args={}):
        mainwin.clear()
        mainwin.refresh()
        self.draw(tab)
        self.tabs[tab].function(mainwin, args)


def main(stdscr):
    curses.curs_set(0)

    from db import Database
    database = Database()
    database.new_session()

    stdscr.refresh()

    # Normal
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # Tab active
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Timer primed
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    # Timer ready
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Active solve
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)

    # Cube color
    # Black
    curses.init_pair(6, 244, curses.COLOR_BLACK)
    # Yellow
    curses.init_pair(7, 226, curses.COLOR_BLACK)
    # Green
    curses.init_pair(8, 46, curses.COLOR_BLACK)
    # Blue
    curses.init_pair(9, 21, curses.COLOR_BLACK)
    # Orange
    curses.init_pair(10, 172, curses.COLOR_BLACK)
    # Red
    curses.init_pair(11, 196, curses.COLOR_BLACK)

    height, width = stdscr.getmaxyx()

    tabs = Tabs(curses.newwin(1, width, 0, 0), curses.color_pair(1), curses.color_pair(2) | curses.A_UNDERLINE)

    mainwin = curses.newwin(height - 1, width, 1, 0)

    algorithm_positions = get_algorithm_positions(*mainwin.getmaxyx())

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
                "database": database})
        elif key == curses.KEY_F2:
            tabs.switch_to("solves", mainwin, args={
                "database": database})
        elif key == curses.KEY_F3:
            tabs.switch_to("chart", mainwin, args={
                "database": database})
        elif key == curses.KEY_F4:
            tabs.switch_to("algorithms", mainwin, args={
                "algorithm_positions": algorithm_positions})


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    curses.endwin()
    print("ctrl-c recieved, exiting...")

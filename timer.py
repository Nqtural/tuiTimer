import curses
import threading
import time
from scramble import scramble
from pynput import keyboard

stop_thread = False
stop_timer = False

scramble_alg = False
timer_time = 0


def turn_timer_green(time, stdscr, timer, decimals, height, width):
    global stop_thread
    for i in range(0, 5):
        if stop_thread: break
        time.sleep(0.1)
    stdscr.clear()
    stdscr.addstr(int(height / 2) - 1, int((width - len(format_timer(timer_time, decimals))) / 2), format_timer(timer_time, decimals), curses.color_pair(4))
    stdscr.refresh()


def listen_for_space(key):
    if key == keyboard.Key.space:
        return False
    if key == keyboard.Key.f2 or key == keyboard.Key.f3 or key == keyboard.Key.f4:
        global stop_timer
        stop_timer = True
        return False


def format_timer(timer_time, decimals):
    if timer_time / 60 > 1: # Show minutes
        return f"   {int(timer_time / 60)}:{'' if timer_time % 60 > 10 else '0'}{(timer_time % 60):.{decimals}f}   "
    else: # Don't show minutes
        return f"   {timer_time:.{decimals}f}   "


def timer(stdscr, args):
    cover = args["cover"]
    decimals = args["decimals"]
    database = args["database"]

    height, width = stdscr.getmaxyx()

    global scramble_alg
    global stop_timer
    global timer_time
    stop_timer = False

    while True:
        timer = 0
        decimals = 3
        stdscr.clear()
        stdscr.addstr(int(height / 2) - 1, int((width - len(format_timer(timer_time, decimals))) / 2), format_timer(timer_time, decimals), curses.color_pair(1))
        if not scramble_alg: 
            scramble_alg = scramble(20)
        stdscr.addstr(int(height / 2) + 1, int((width - len(scramble_alg)) / 2), scramble_alg)

        last_five = [solve[2] for solve in database.read(5)]
        if len(last_five) >= 5:
            stdscr.addstr(height - 1, 0, f"Ao5: {format_timer(sum(last_five) / 5, decimals).replace('   ', '')}")

        stdscr.refresh()

        with keyboard.Listener(
            on_press=listen_for_space) as listener:
            listener.join()

        if stop_timer: break

        stdscr.clear()
        stdscr.addstr(int(height / 2) - 1, int((width - len(format_timer(timer_time, decimals))) / 2), format_timer(timer_time, decimals), curses.color_pair(3))
        stdscr.refresh()

        thread = threading.Thread(target=turn_timer_green, args=(time, stdscr, timer_time, decimals, height, width))
        thread.start()

        with keyboard.Listener(
            on_release=listen_for_space) as listener:
            listener.join()

        if stop_timer: break

        if thread.is_alive():
            stdscr.addstr(int(height / 2) - 1, int((width - len(format_timer(timer_time, decimals))) / 2), format_timer(timer_time, decimals), curses.color_pair(1))
            stdscr.refresh()
            global stop_thread
            stop_thread = True
            thread.join()
            stop_thread = False
            continue

        start = time.time()

        listener = keyboard.Listener(
            on_press=listen_for_space)
        listener.start()

        if stop_timer: break

        if cover:
            stdscr.clear()
            stdscr.addstr(int(height / 2) - 1, int((width - len("Solve")) / 2), "Solve")
            stdscr.refresh()

        else:
            stdscr.clear()
            while listener.is_alive():
                timer_time = time.time() - start
                stdscr.addstr(
                    int(height / 2) - 1,
                    int((width - len(format_timer(timer_time, decimals))) / 2),
                    format_timer(timer_time, decimals),
                    curses.color_pair(1))
                stdscr.refresh()

        listener.join()

        timer_time = time.time() - start
        database.write(f"{timer_time:.3f}", scramble_alg)
        scramble_alg = False



def main():
    from parser import parse_args
    args = parse_args()
    if args.scramble:
        print(scramble(20))
    else:
        try:
            curses.wrapper(timer, args.cover, args.decimals)
        except KeyboardInterrupt:
            curses.endwin()
            print("Ctrl-c recieved, exiting...")


if __name__ == "__main__": main()

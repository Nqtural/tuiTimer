import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="tuiTimer",
        description="Speedcubing timer inspired by csTimer in a TUI ")

    parser.add_argument("-s", "--session", help="resume a previous session")

    return parser.parse_args()

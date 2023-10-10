import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="speedcube-cli",
        description="Small program for speedcubing")

    parser.add_argument("-s", "--scramble", action="store_true", help="only output a scramble algorithm")
    parser.add_argument("-c", "--cover", action="store_true", help="cover timer while solving")
    parser.add_argument("-d", "--decimals", type=int, default=3, choices=range(0, 4), help="number of decimals to use (max 3)")

    return parser.parse_args()

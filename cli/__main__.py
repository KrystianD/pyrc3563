import argparse

from rc3563 import RC3563


def main():
    argparser = argparse.ArgumentParser(prog="python -m cli")
    argparser.add_argument("path", help="Serial port path")

    args = argparser.parse_args()

    rc = RC3563(args.path)
    while True:
        pkt = rc.read()
        print(f"V: {pkt.voltage_v:.3f}, R: {pkt.resistance_ohm:.6f}")


main()

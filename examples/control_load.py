import argparse
import asyncio
import logging
import sys
import termios
import tty
from contextlib import contextmanager
from typing import Iterator, Optional

from aiovantage import Vantage


# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def parse_keypress() -> Optional[str]:
    # Rudimentary keypress parser

    c = sys.stdin.read(1)
    if c == "\x1b":
        seq = sys.stdin.read(2)
        if seq == "[A":
            return "KEY_UP"
        elif seq == "[B":
            return "KEY_DOWN"
        else:
            return None
    else:
        return c


@contextmanager
def cbreak_mode(fd: int) -> Iterator[None]:
    # Context manager to read terminal input character by character

    old_attrs = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(args.host, args.username, args.password) as vantage:
        # Print out the available loads
        print("Load ID  Name")
        print("-------  ----")
        async for load in vantage.loads:
            print(f"{load.id: ^7}  {load.name}")
        print()

        # Ask which load to control
        while True:
            try:
                print("Enter a load ID to control:")
                print("> ", end="", flush=True)

                load_id = int(input())
                load = vantage.loads[load_id]
                break
            except (ValueError, KeyError):
                print("Invalid load id")
                continue

        # Print control instructions
        print(f"\nControlling load '{load.name}'")
        print("    Use the arrow keys to increase or decrease the load's brightness.")
        print("    Press the spacebar to toggle the load.")
        print("    Press 'q' to quit.\n")

        # Listen for control keypresses
        with cbreak_mode(sys.stdin.fileno()):
            while True:
                key = parse_keypress()
                level = load.level or 0

                if key == "KEY_UP":
                    # Increase the load's brightness
                    await vantage.loads.set_level(load.id, level + 10, transition=1)
                    print(f"Increased '{load.name}' brightness to {load.level}%")

                elif key == "KEY_DOWN":
                    # Decrease the load's brightness
                    await vantage.loads.set_level(load.id, level - 10, transition=1)
                    print(f"Decreased '{load.name}' brightness to {load.level}%")

                elif key == " ":
                    # Toggle load
                    if load.is_on:
                        await vantage.loads.turn_off(load.id)
                        print(f"Turned '{load.name}' load off")
                    else:
                        await vantage.loads.turn_on(load.id)
                        print(f"Turned '{load.name}' load on")

                elif key == "q":
                    break


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

import argparse
import asyncio
import logging
import sys
import termios
from contextlib import contextmanager
from enum import Enum
from typing import Iterator, TextIO, Union

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


Key = Enum("Key", ["UP", "DOWN"])


def parse_keypress() -> Union[Key, str, None]:
    c = sys.stdin.read(1)
    if c == "\x1b":
        seq = sys.stdin.read(2)
        if seq == "[A":
            return Key.UP
        elif seq == "[B":
            return Key.DOWN
        else:
            return None
    else:
        return c


@contextmanager
def raw_mode(io: TextIO) -> Iterator[None]:
    old_attrs = termios.tcgetattr(io)
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(io, termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(io, termios.TCSADRAIN, old_attrs)


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(args.host, args.username, args.password) as vantage:
        # Print out the available loads
        print("Available loads:")
        async for load in vantage.loads:
            print(f"{load.id} | {load.name}")
        print()

        # Ask which load to control
        while True:
            try:
                print("Enter a load ID to control:")
                print("> ", end="", flush=True)
                load_id = int(input())
                load = vantage.loads[load_id]
                print()
                break
            except (ValueError, KeyError):
                print("Invalid load id\n")
                continue

        # Print control instructions
        print(f"Controlling load '{load.name}'")
        print("    Use the arrow keys to increase or decrease the load's brightness.")
        print("    Press the spacebar to toggle the load.")
        print("    Press 'q' to quit.\n")

        # Listen for control keypresses
        with raw_mode(sys.stdin):
            while True:
                key = parse_keypress()
                level = load.level or 0
                if key == Key.UP:
                    # Increase the load's brightness
                    await vantage.loads.set_level(load.id, level + 10, transition=1)
                    print(f"Increased '{load.name}' brightness to {load.level}%")
                elif key == Key.DOWN:
                    # Decrease the load's brightness
                    await vantage.loads.set_level(load.id, level - 10, transition=1)
                    print(f"Decreased '{load.name}' brightness to {load.level}%")
                elif key == " ":
                    # Toggle load
                    if level > 0:
                        await vantage.loads.set_level(load.id, 0, transition=1)
                        print(f"Turned '{load.name}' load off")
                    else:
                        await vantage.loads.set_level(load.id, 100)
                        print(f"Turned '{load.name}' load on")
                elif key == "q":
                    break


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

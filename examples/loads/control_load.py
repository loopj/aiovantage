"""Print a list of loads and allow the user to control them with the keyboard."""

import argparse
import asyncio
import logging
import sys
import termios
import tty
from collections.abc import Iterator
from contextlib import contextmanager, suppress

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


async def parse_keypress() -> str | None:
    """Rudimentary keypress parser (async version)."""
    loop = asyncio.get_running_loop()
    char: str = await loop.run_in_executor(None, sys.stdin.read, 1)
    if char == "\x1b":
        seq = await loop.run_in_executor(None, sys.stdin.read, 2)
        if seq == "[A":
            return "KEY_UP"
        if seq == "[B":
            return "KEY_DOWN"
        return None
    return char


@contextmanager
def cbreak_mode(descriptor: int) -> Iterator[None]:
    """Context manager to read terminal input character by character."""
    old_attrs = termios.tcgetattr(descriptor)
    try:
        tty.setcbreak(descriptor)
        yield
    finally:
        termios.tcsetattr(descriptor, termios.TCSADRAIN, old_attrs)


def clamp(value: int, min_value: int, max_value: int) -> int:
    """Clamp a value between a minimum and maximum value."""
    return max(min_value, min(max_value, value))


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(
        args.host, args.username, args.password, ssl=args.ssl
    ) as vantage:
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
                key = await parse_keypress()

                if key == "KEY_UP" or key == "KEY_DOWN":
                    # Increase or decrease load brightness
                    level = int(load.level or 0)
                    new_level = clamp(level + (10 if key == "KEY_UP" else -10), 0, 100)
                    if new_level == level:
                        continue

                    await load.ramp(load.RampType.Fixed, 1, new_level)
                    print(f"Set '{load.name}' brightness to {new_level}%")

                elif key == " ":
                    # Toggle load
                    if load.is_on:
                        await load.turn_off()
                        print(f"Turned '{load.name}' load off")
                    else:
                        await load.turn_on()
                        print(f"Turned '{load.name}' load on")

                elif key == "q":
                    break


with suppress(KeyboardInterrupt):
    asyncio.run(main())

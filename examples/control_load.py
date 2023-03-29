#!/usr/bin/env python3

from os.path import abspath, dirname
from sys import path

path.insert(1, dirname(dirname(abspath(__file__))))

import asyncio
import sys
import termios
import tty

from aiovantage import Vantage


async def main() -> None:
    vantage = Vantage("10.2.0.103", "administrator", "ZZuUw76CnL")
    await vantage.connect()
    await vantage.loads.fetch_objects()

    try:
        print("Available loads:")
        for load in vantage.loads:
            print(f"{load.id} | {load.name}")
        print()

        # Prompt for the load ID
        sys.stdout.write("Enter a load ID to control: ")
        sys.stdout.flush()
        load_id = int(input())
        load = vantage.loads[load_id]

        # Suppress echoing
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

        # Print instructions to the user
        print("Use the arrow keys to increase or decrease the load's brightness.")
        print("Press the spacebar to toggle the load.")
        print("Press 'q' to quit.\n")

        # Main loop
        while True:
            # Get the next key pressed
            c = sys.stdin.read(1)

            # Check if the key is an escape sequence
            if c == "\x1b":
                # Read the rest of the escape sequence
                seq = sys.stdin.read(2)
                if seq == "[A":  # Up arrow
                    # Increase the load's brightness
                    level = await load.get_level()
                    await load.set_level(level + 10)
                elif seq == "[B":  # Down arrow
                    # Decrease the load's brightness
                    level = await load.get_level()
                    await load.set_level(level - 10)
            elif c == " ":
                # Toggle load
                level = await load.get_level()
                if level > 0:
                    await load.set_level(0)
                else:
                    await load.set_level(100)
            elif c == "q":
                break

    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

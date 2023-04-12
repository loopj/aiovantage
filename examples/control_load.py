#!/usr/bin/env python3

import asyncio
import logging
import sys
import termios
import tty

from aiovantage import Vantage

logging.basicConfig(level=logging.DEBUG)

async def main() -> None:
    vantage = Vantage("10.2.0.103", "administrator", "ZZuUw76CnL")
    await vantage.connect()
    await vantage.loads.initialize()

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
                    level = await vantage.loads.get_level(load_id)
                    await vantage.loads.set_level(load_id, level + 10)
                elif seq == "[B":  # Down arrow
                    # Decrease the load's brightness
                    level = await vantage.loads.get_level(load_id)
                    await vantage.loads.set_level(load_id, level - 10)
            elif c == " ":
                # Toggle load
                level = await vantage.loads.get_level(load_id)
                if level > 0:
                    await vantage.loads.set_level(load_id, 0)
                else:
                    await vantage.loads.set_level(load_id, 100)
            elif c == "q":
                break

    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

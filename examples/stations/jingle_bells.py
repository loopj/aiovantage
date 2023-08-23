"""Play Jingle Bells on the sounder of a Vantage keypad."""

import argparse
import asyncio

from aiovantage import Vantage
from aiovantage.command_client.object_interfaces import SounderInterface

JINGLE_BELLS = [
    ("E", 0.25),
    ("E", 0.25),
    ("E", 0.5),
    ("E", 0.25),
    ("E", 0.25),
    ("E", 0.5),
    ("E", 0.25),
    ("G", 0.25),
    ("C", 0.25),
    ("D", 0.25),
    ("E", 1),
    ("F", 0.25),
    ("F", 0.25),
    ("F", 0.5),
    ("F", 0.125),
    ("F", 0.125),
    ("E", 0.25),
    ("E", 0.5),
    ("E", 0.125),
    ("E", 0.125),
    ("E", 0.125),
    ("D", 0.25),
    ("D", 0.25),
    ("E", 0.25),
    ("D", 0.5),
    ("G", 0.5),
]

FREQUENCIES = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
}

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("id", help="keypad id to play sound on")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    """Play Jingle Bells on the sounder of a Vantage keypad."""
    async with Vantage(args.host, args.username, args.password) as vantage:
        sounder = SounderInterface(vantage.command_client)

        # Turn on the sounder
        await sounder.turn_on(args.id)

        # Play each note in Jingle Bells
        for note, duration in JINGLE_BELLS:
            frequency = FREQUENCIES[note]
            await sounder.set_frequency(args.id, frequency)
            await asyncio.sleep(duration)

        # Turn off the sounder
        await sounder.turn_off(args.id)


asyncio.run(main())

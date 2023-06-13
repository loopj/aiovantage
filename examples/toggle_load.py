import argparse
import asyncio
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("id", help="load id to toggle")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller and print out the name and value of each GMem
    async with Vantage(args.host, args.username, args.password) as vantage:
        try:
            load_id = int(args.id)
        except ValueError:
            print("Invalid load id")
            return

        load = await vantage.loads.aget(load_id)
        if load is None:
            print("Load not found")
            return

        print(f"Toggling {load.name} (id = {load.id})")
        if load.is_on:
            await vantage.loads.turn_off(load.id)
        else:
            await vantage.loads.turn_on(load.id)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

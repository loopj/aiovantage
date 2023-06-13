import argparse
import asyncio
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller and print out details of each blind group
    async with Vantage(args.host, args.username, args.password) as vantage:
        async for blind_group in vantage.blind_groups:
            print(blind_group)
            print(f"[{blind_group.id}] '{blind_group.name}' {blind_group.blind_ids}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

import argparse
import asyncio
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--no-ssl", help="use non-ssl connection", action="store_true")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller and print out the name and level of each load
    async with Vantage(
        args.host, args.username, args.password, use_ssl=not args.no_ssl
    ) as vantage:
        async for load in vantage.loads:
            print(f"{load.name} - {load.level}%")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

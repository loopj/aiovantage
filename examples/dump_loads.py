import argparse
import asyncio

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Fetch loads from the controller
        await vantage.loads.initialize()

        # Print out the name of each load
        for load in vantage.loads:
            print(f"{load.name}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

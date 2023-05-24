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

# Some ANSI escape codes for pretty printing
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller and print out the name and level of each load
    async with Vantage(args.host, args.username, args.password) as vantage:
        async for load in vantage.loads:
            print(
                f"- {load.name} "
                + (
                    f"{GREEN}({load.level}%){RESET}"
                    if load.level
                    else f"{RED}(OFF){RESET}"
                )
            )


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

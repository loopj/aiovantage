"""Set the value of a variable on the Vantage controller."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("id", help="GMem id to set")
parser.add_argument("value", help="value to set GMem to")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(
        args.host, args.username, args.password, ssl=args.ssl
    ) as vantage:
        # Look up the object by id
        try:
            gmem_id = int(args.id)
            gmem = await vantage.gmem.aget(gmem_id)
            if gmem is None:
                print(f"GMem object with id '{gmem_id}' does not exist")
                return
        except ValueError:
            print(f"Couldn't parse object id '{args.id}'")
            return

        # Convert the value to the correct type
        if gmem.is_bool:
            if args.value.lower() in ("true", "1", "on"):
                args.value = True
            elif args.value.lower() in ("false", "0", "off"):
                args.value = False
            else:
                print("Invalid boolean value")
                return
        elif gmem.is_int:
            try:
                args.value = int(args.value)
            except ValueError:
                print("Invalid integer value")
                return

        # Set the value
        print(f"Setting '{gmem.name}' (id = {gmem.id}) to '{args.value}'")
        await gmem.set_value(args.value)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())

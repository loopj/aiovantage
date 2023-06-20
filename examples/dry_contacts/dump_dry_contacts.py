"""Prints out the id and name of each dry contact in the Vantage controller."""

import asyncio
import contextlib
from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Print some details about each dry contact
        async for dry_contact in vantage.dry_contacts:
            print(f"[{dry_contact.id}] name='{dry_contact.name}' ")


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)

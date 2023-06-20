"""Set the value of a variable on the Vantage controller."""

import asyncio
import contextlib

from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Connect to the Vantage controller and print out the name and value of each GMem
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Look up the object by id
        try:
            gmem_id = int(args.id)
            gmem = await vantage.gmem.aget(gmem_id)
            if gmem is None:
                print(f"GMem object with id '{gmem_id}' does not exist")
                return
        except ValueError:
            print(f"Couldn't parse object id 'gmem_id'")
            return

        # Convert the value to the correct type
        # TODO: Unresolved attribute reference 'lower' for class 'bool'
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
        await vantage.gmem.set_value(gmem_id, args.value)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)

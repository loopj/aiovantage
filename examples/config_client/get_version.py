"""Example of using the ConfigClient to get the Vantage version."""
import asyncio
import contextlib

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.introspection import GetVersion

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    async with ConfigClient(args.host, args.username, args.password) as client:
        # Simple RPC request without any params (IIntrospection.GetVersion)
        version = await client.request(GetVersion)
        print(version)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)

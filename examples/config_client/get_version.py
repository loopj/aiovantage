import argparse
import asyncio
import logging

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.introspection import GetVersion


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

    async with ConfigClient(args.host, args.username, args.password) as client:
        # Simple RPC request without any params (IIntrospection.GetVersion)
        version = await client.request(GetVersion)
        print(version)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

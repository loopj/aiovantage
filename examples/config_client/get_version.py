import argparse
import asyncio

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.interfaces import IIntrospection
from aiovantage.config_client.methods.introspection import GetVersion


# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--no-ssl", help="use non-ssl connection", action="store_true")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    async with ConfigClient(
        args.host, args.username, args.password, use_ssl=not args.no_ssl
    ) as client:
        # Simple RPC request without any params (IIntrospection.GetVersion)
        version = await client.request(IIntrospection, GetVersion)
        print(version)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

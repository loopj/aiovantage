"""Example of reading the trigger history, system log and module status."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.config_client import ConfigClient, DiagnosticInterface

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with ConfigClient(
        args.host, args.username, args.password, ssl=args.ssl
    ) as client:
        # Which object started which task, as shown in the Diagnostics "History"
        print("# Trigger history")
        for entry in await DiagnosticInterface.get_event_log(client):
            print(
                entry.time_stamp,
                entry.trigger_type.name
                if entry.trigger_type is not None
                else entry.event,
                f"{entry.source} -> {entry.destination}",
                entry.param1,
                entry.param2,
            )
        print()

        # The system log, as shown in the Diagnostics "Log"
        print("# System log")
        for entry in await DiagnosticInterface.get_sys_log(client):
            log_type = entry.log_type.name if entry.log_type is not None else entry.type
            print(entry.time, log_type, entry.src, entry.msg)
        print()

        # The modules responding on the first enclosure's bus
        print("# Modules")
        for module in await DiagnosticInterface.get_modules(client):
            print(module.address, module.vid, module.model, module.errors)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())

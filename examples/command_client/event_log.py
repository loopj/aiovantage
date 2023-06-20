"""Example of using the CommandClient to subscribe to system log events."""

import asyncio
import contextlib

from aiovantage.command_client import CommandClient, Event, EventType

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


def command_client_callback(event: Event) -> None:
    """Print out the log message for each event."""
    if event["tag"] == EventType.EVENT_LOG:
        print(event["log"])
    elif event["tag"] == EventType.CONNECTED:
        print("Connected and monitoring for log events...")


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Create a Host Command client
    async with CommandClient(args.host, args.username, args.password) as client:
        # Subscribe to connection events
        client.subscribe(command_client_callback, EventType.CONNECTED)

        # Subscribe to system log events
        await client.subscribe_event_log(command_client_callback, "SYSTEM")

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)

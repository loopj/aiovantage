"""Use a CommandClient to subscribe to status updates for LOAD objects."""

import asyncio
import contextlib

from aiovantage.command_client import CommandClient, Event, EventType

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


def command_client_callback(event: Event) -> None:
    """Print out the status update for each event."""
    if event["tag"] == EventType.STATUS:
        print(f"[{event['status_type']}] id: {event['id']}, args: {event['args']}")
    elif event["tag"] == EventType.CONNECTED:
        print("Connected and monitoring for status updates...")
    elif event["tag"] == EventType.DISCONNECTED:
        print("Disconnected")
    elif event["tag"] == EventType.RECONNECTED:
        print("Reconnected")


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Create a Host Command client
    async with CommandClient(args.host, args.username, args.password) as client:
        # Subscribe to connection events
        client.subscribe(
            command_client_callback,
            (EventType.CONNECTED, EventType.DISCONNECTED, EventType.RECONNECTED),
        )

        # Subscribe to status updates for LOAD objects (STATUS LOAD)
        await client.subscribe_status(command_client_callback, "LOAD")

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)

# Host Command Service Client

This module provides a client for the Vantage Host Command service.

This module is stateless and has no knowledge of the configuration of a Vantage system,
and should typically be used alongside a `ConfigClient`, or using the higher level
controller interfaces.

The Host Command service is a text-based service that allows interaction with devices
controlled by a Vantage InFusion Controller.

Among other things, this service allows you to change the state of devices
(eg. turn on/off a light) as well as subscribe to status changes for devices.

This module provides classes for connecting to the Host Command service, sending
commands, and receiving events. It also provides helper methods for subscribing to
various types of events, such as "STATUS" and "ELLOG".

Connections are created lazily when needed, and closed when the client is closed,
and will automatically reconnect if the connection is lost.

## Examples

### Get the controller firmware version

```python
from aiovantage.command_client import CommandClient

async with CommandClient("10.2.0.103") as client:
    # Get the controller firmware version
    v = await client.command("VERSION").args[0]
```

### Turn on a load

```python
from aiovantage.command_client import CommandClient

async with CommandClient("10.2.0.103") as client:
    # Set load with id 118 to 100%
    await client.command("LOAD", 118, 100)
```

### Subscribe to load events

```python
from aiovantage.command_client import Event, EventStream, EventType

def callback(event: Event) -> None:
    assert event["type"] == EventType.STATUS
    print(f"Load {event['id']} changed state")

events = EventStream("10.2.0.103")
events.subscribe_status(callback, "LOAD")
```

# aiovantage

[![Documentation](https://img.shields.io/badge/Documentation-8CA1AF?style=for-the-badge&logo=readthedocs&logoColor=fff)](https://aiovantage.readthedocs.io)
[![PyPI - Version](https://img.shields.io/pypi/v/aiovantage?style=for-the-badge)](https://pypi.org/project/aiovantage/)
[![Discord](https://img.shields.io/discord/1120862286576353370?style=for-the-badge)](https://discord.gg/psU7PxDyNQ)

Python library for interacting with and controlling Vantage InFusion home automation controllers.

This open-source, non-commercial library is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Vantage, and is provided for interoperability purposes only.

## Example

```python
from aiovantage import Vantage

async with Vantage("192.168.1.2", "username", "password") as vantage:
    async for load in vantage.loads:
        print(f"{load.name} is at {load.level}%")
```

See the [examples](https://github.com/loopj/aiovantage/tree/main/examples) folder for more examples.

## Features

- Fetch object *configuration* from your Vantage system.
- Fetch object *state* and subscribe to state changes (e.g. load levels, sensor readings).
- Control devices (turn on lights, set thermostats, etc).
- Uses `asyncio` for non-blocking I/O.
- Uses SSL connections by default, with automatic reconnection.
- Supports both lazy and eager object fetching.

## Installation

Add `aiovantage` as a dependency to your project, or install it directly:

```shell
pip install aiovantage
```

## Supported objects

The following interfaces/controllers are currently supported.

| Type          | Description           | Controller                    |
| ------------- | --------------------- | ----------------------------- |
| AnemoSensor   | Wind speed sensors    | `vantage.anemo_sensors`       |
| Area          | Rooms, etc            | `vantage.areas`               |
| BackBox       | Backboxes             | `vantage.back_boxes`          |
| Blind         | Shades, blinds        | `vantage.blinds`              |
| BlindGroups   | Groups of blinds      | `vantage.blind_groups`        |
| Buttons       | Keypad buttons        | `vantage.buttons`             |
| DryContacts   | Motion sensors, etc   | `vantage.dry_contacts`        |
| GMem          | Vantage variables     | `vantage.gmem`                |
| LightSensor   | Light sensors         | `vantage.light_sensors`       |
| Load          | Lights, relays, etc   | `vantage.loads`               |
| LoadGroup     | Groups of loads       | `vantage.load_groups`         |
| Master        | Vantage controllers   | `vantage.masters`             |
| Module        | Dimmer modules        | `vantage.modules`             |
| OmniSensor    | Power, current, etc   | `vantage.omni_sensors`        |
| PortDevice    | Port devices (hubs)   | `vantage.port_devices`        |
| PowerProfile  | Load power profiles   | `vantage.power_profiles`      |
| RGBLoad       | RGB lights            | `vantage.rgb_loads`           |
| Stations      | Keypads, etc          | `vantage.stations`            |
| Tasks         | Vantage tasks         | `vantage.tasks`               |
| Temperature   | Temperature sensors   | `vantage.temperatures`        |
| Thermostat    | Thermostats           | `vantage.thermostats`         |

If you have an object that you expect to show up in one of these controllers but is missing, please [create an issue](https://github.com/loopj/aiovantage/issues) or [submit a pull request](https://github.com/loopj/aiovantage/pulls).

## Usage

### Creating a client

Begin by importing the `Vantage` class:

```python
from aiovantage import Vantage
```

The most convenient way to create a client is by using the async context manager:

```python
async with Vantage("hostname", "username", "password") as vantage:
    # ...use the vantage client
```

Alternatively, you can manage the lifecycle of the client yourself:

```python
from aiovantage import Vantage

vantage = Vantage("hostname", "username", "password")
# ...use the vantage client
vantage.close()
```

### Querying objects

The `Vantage` class exposes a number of *controllers*, which can be used to query objects. Controllers can either be populated lazily (by using `async for`), or eagerly (by using `controller.initialize()`).

For example, to get a list of all loads:

```python
async with Vantage("hostname", "username", "password") as vantage:
    async for load in vantage.loads:
        print(f"{load.name} is at {load.level}%")
```

Alternatively, you can use `controller.initialize()` to eagerly fetch all objects:

```python
async with Vantage("hostname", "username", "password") as vantage:
    await vantage.loads.initialize()
    for load in vantage.loads:
        print(f"{load.name} is at {load.level}%")
```

If you aren't interested in the state of the objects, you can call `controller.initialize(fetch_state=False)` to slightly speed up the initialization:

```python
async with Vantage("hostname", "username", "password") as vantage:
    await vantage.loads.initialize(fetch_state=False)
    for load in vantage.loads:
        print(f"{load.name}")
```

All controllers implement a django-like query interface, which can be used to filter objects. You can either query by matching attributes:

```python
async with Vantage("hostname", "username", "password") as vantage:
    async for load in vantage.loads.filter(name="Kitchen"):
        print(f"{load.name} is at {load.level}%")
```

Or by using a filter predicate:

```python
async with Vantage("hostname", "username", "password") as vantage:
    async for load in vantage.loads.filter(lambda load: load.level > 50):
        print(f"{load.name} is at {load.level}%")
```

### Fetching a single object

You can fetch a single object by id, by calling `controller.aget()` or `controller.get()`:

```python
async with Vantage("hostname", "username", "password") as vantage:
    load = await vantage.loads.aget(118)
    print(f"{load.name} is at {load.level}%")
```

These functions also implement the same query interface as `controller.filter()` for querying by
attributes or filter predicate:

```python
async with Vantage("hostname", "username", "password") as vantage:
    load = await vantage.loads.aget(name="Kitchen")
    print(f"{load.name} is at {load.level}%")
```

### Controlling objects

Objects also expose various methods for controlling state. For example, to turn on a load:

```python
async with Vantage("hostname", "username", "password") as vantage:
    load = vantage.loads.aget(name="Study Lights")
    await load.turn_on()
```

### Subscribing to state changes

You can subscribe to state changes by using the `controller.subscribe()` method:

```python
def on_load_state_change(event, load, data):
    print(f"{load.name} is at {load.level}%")

async with Vantage("hostname", "username", "password") as vantage:
    vantage.loads.subscribe(on_load_state_change)
    await vantage.loads.initialize()
```

Note that a subscription will only receive state changes for objects that have populated into the controller.

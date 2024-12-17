# aiovantage

aiovantage is a Python library for interacting with and controlling Vantage InFusion home automation controllers.

Uses a *controller* pattern inspired heavily by the [aiohue](https://github.com/home-assistant-libs/aiohue) library.

This open-source, non-commercial library is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Vantage, and is provided for interoperability purposes only.

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Example](#example)
- [Features](#features)
- [Supported objects types](#supported-objects-types)
- [Installation](#installation)
- [Usage](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Example

```python
from aiovantage import Vantage

async with Vantage("192.168.1.2", "username", "password") as vantage:
    async for load in vantage.loads:
        print(f"{load.name} is at {load.level}%")
```

See the [examples](examples) folder for more examples.

## Features

- Uses Python asyncio for non-blocking I/O.
- Exposes "controllers" to make fetching and controlling various objects easy.
- Uses SSL connections by default, with automatic reconnection.
- Fetch objects lazily (with `async for obj in controller`).
- Alternatively, eager-fetch objects with `controller.initialize`.

## Supported objects types

The following interfaces/controllers are currently supported.

| Type          | Description           | Controller                    | Examples                                  |
| ------------- | --------------------- | ----------------------------- | ----------------------------------------- |
| AnemoSensor   | Wind speed sensors    | `vantage.anemo_sensors`       | [Examples](examples/anemo_sensors)        |
| Area          | Rooms, etc            | `vantage.areas`               | [Examples](examples/areas)                |
| BackBox       | Backboxes             | `vantage.backboxes`           |                                           |
| Blind         | Shades, blinds        | `vantage.blinds`              | [Examples](examples/blinds)               |
| BlindGroups   | Groups of blinds      | `vantage.blind_groups`        | [Examples](examples/blind_groups)         |
| Buttons       | Keypad buttons        | `vantage.buttons`             | [Examples](examples/buttons)              |
| DryContacts   | Motion sensors, etc   | `vantage.dry_contacts`        | [Examples](examples/dry_contacts)         |
| GMem          | Vantage variables     | `vantage.gmem`                | [Examples](examples/gmem)                 |
| LightSensor   | Light sensors         | `vantage.light_sensors`       | [Examples](examples/light_sensors)        |
| Load          | Lights, relays, etc   | `vantage.loads`               | [Examples](examples/loads)                |
| LoadGroup     | Groups of loads       | `vantage.load_groups`         | [Examples](examples/load_groups)          |
| Master        | Vantage controllers   | `vantage.masters`             | [Examples](examples/masters)              |
| Module        | Dimmer modules        | `vantage.modules`             |                                           |
| OmniSensor    | Power, current, etc   | `vantage.omni_sensors`        | [Examples](examples/omni_sensors)         |
| PortDevice    | Port devices (hubs)   | `vantage.port_devices`        |                                           |
| PowerProfile  | Load power profiles   | `vantage.power_profiles`      | [Examples](examples/power_profiles)       |
| RGBLoad       | RGB lights            | `vantage.rgb_loads`           | [Examples](examples/rgb_loads)            |
| Stations      | Keypads, etc          | `vantage.stations`            | [Examples](examples/stations)             |
| Tasks         | Vantage tasks         | `vantage.tasks`               | [Examples](examples/tasks)                |
| Temperature   | Temperature sensors   | `vantage.temperature_sensors` | [Examples](examples/temperature_sensors)  |
| Thermostat    | Thermostats           | `vantage.thermostats`         | [Examples](examples/thermostats)          |

If you have an object that you expect to show up in one of these controllers but is missing, please [create an issue](issues) or [submit a pull request](CONTRIBUTING.md#-adding-support-for-new-devices).

## Installation

Add `aiovantage` as a dependency to your project, or install it directly:

```shell
pip install aiovantage
```

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

Most controllers expose a various methods for controlling the state of objects. The first parameter to these methods is always the vantage id of the object to control.

For example, to turn on a load:

```python
async with Vantage("hostname", "username", "password") as vantage:
    await vantage.loads.turn_on(118)
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

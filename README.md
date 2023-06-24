# aiovantage

aiovantage is a Python library for interacting with and controlling Vantage InFusion home automation controllers.

Uses a "controller" pattern inspired heavily by the [aiohue](https://github.com/home-assistant-libs/aiohue) library.

This open-source, non-commercial library is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Vantage, and is provided for interoperability purposes only.


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
| Blind         | Shades, blinds        | `vantage.blinds`              | [Examples](examples/blinds)               |
| BlindGroups   | Groups of blinds      | `vantage.blind_groups`        | [Examples](examples/blind_groups)         |
| Buttons       | Keypad buttons        | `vantage.buttons`             | [Examples](examples/buttons)              |
| DryContacts   | Motion sensors, etc   | `vantage.dry_contacts`        | [Examples](examples/dry_contacts)         |
| GMem          | Vantage variables     | `vantage.gmem`                | [Examples](examples/gmem)                 |
| LightSensor   | Light sensors         | `vantage.light_sensors`       | [Examples](examples/light_sensors)        |
| Load          | Lights, relays, etc   | `vantage.loads`               | [Examples](examples/loads)                |
| LoadGroup     | Groups of loads       | `vantage.load_groups`         | [Examples](examples/load_groups)          |
| OmniSensor    | Power, current, etc   | `vantage.omni_sensors`        | [Examples](examples/omni_sensors)         |
| RGBLoad       | RGB lights            | `vantage.rgb_loads`           | [Examples](examples/rgb_loads)            |
| Stations      | Keypads, etc          | `vantage.stations`            | [Examples](examples/stations)             |
| Tasks         | Vantage tasks         | `vantage.tasks`               | [Examples](examples/tasks)                |
| Temperature   | Temperature sensors   | `vantage.temperature_sensors` | [Examples](examples/temperature_sensors)  |

If you have an object that you expect to show up in one of these controllers, but it is missing, please let me know in an issue.


## Installation

```shell
pip3 install aiovantage
```
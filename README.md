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

See the [examples](https://github.com/loopj/aiovantage/tree/main/examples) folder for more examples.

## Features
- Uses Python asyncio for non-blocking I/O.
- Exposes "controllers" to make fetching and controlling various objects easy.
- Uses SSL connections by default, with automatic reconnection.
- Fetch objects lazily (with `async for obj in controller`).
- Alternatively, eager-fetch objects with `controller.initialize`.

## Supported objects/controllers
- Areas (rooms, etc) - `vantage.areas`
- Blinds (blinds and shades) - `vantage.blinds`
- BlindGroups (groups of blinds/shades) - `vantage.blind_groups`
- Buttons - `vantage.buttons`
- DryContacts (motion sensors, etc) - `vantage.dry_contacts`
- GMem (variables) - `vantage.gmem`
- Loads (lights, relays, etc) - `vantage.loads`
- LoadGroups (groups of Loads) - `vantage.load_groups`
- OmniSensors (power, current, etc) - `vantage.omni_sensors`
- RGBLoads (RGB lights) - `vantage.rgb_loads`
- Stations (keypads, etc) - `vantage.stations`
- Tasks - `vantage.tasks`

## Installation

```
pip install git+https://github.com/loopj/aiovantage.git
```

# Application Communication Interface Service Client

This module provides a client for the Vantage Application Communication Interface
(ACI) service.

The ACI service is an XML-based RPC service that Design Center uses to communicate
with Vantage InFusion Controllers. There are a number of "interfaces" exposed, each
with one or more "methods".

The `ConfigClient` class handles connecting to the ACI service, authenticating, and the
serialization/deserialization of XML requests and responses.

A (non-exhaustive) set of RPC methods are exposed in the following interface
namespace classes:

- `ConfigurationInterface`
- `IntrospectionInterface`
- `LoginInterface`

## Examples

### Lookup objects by type

```python
from aiovantage.config_client import ConfigClient, ConfigurationInterface

async with ConfigClient("hostname") as client:
    async for obj in ConfigurationInterface.get_objects(client, "Load", "Button"):
        print(obj)
```

### Lookup objects by id, using a helper

```python
from aiovantage.config_client import ConfigClient, ConfigurationInterface

async with ConfigClient("hostname") as client:
    for obj in await ConfigurationInterface.get_object(client, 118):
        print(obj)
```

### Fetch controller version information

```python
from aiovantage.config_client import ConfigClient, IntrospectionInterface

async with ConfigClient("hostname") as client:
    version = await IntrospectionInterface.get_version(client)
```

### Authenticate an ACI client session

```python
from aiovantage.config_client import ConfigClient, LoginInterface

async with ConfigClient("hostname") as client:
    await LoginInterface.login(client, "username", "password")
```

### Make a raw request

```python
from aiovantage.config_client import ConfigClient

async with ConfigClient("hostname") as client:
    response = await client.raw_request("<IIntrospection><GetVersion></GetVersion></IIntrospection>", "</IIntrospection>")

```

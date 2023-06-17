# Application Communication Interface Service Client

This module provides a client for the Vantage Application Communication Interface
(ACI) service.

The ACI service is an XML-based RPC service that Design Center uses to communicate
with Vantage InFusion Controllers. There are a number of "interfaces" exposed, each
with one or more "methods".

The `ConfigClient` class handles connecting to the ACI service, authenticating, and the
serialization/deserialization of XML requests and responses.

Various pre-defined method classes are available in [`methods`](methods) to help with
creating XML serialized requests, but it is also possible to make raw XML requests to
a particular interface.

Since a common use case for interacting with the ACI service is to lookup system
objects, this module also provides models to help with deserializing many of these
object types, available in [`objects`](objects).

Additionally, a few helper functions for fetching objects are provided by
[`helpers.py`](helpers.py).


## Examples

### Lookup objects by type, using a helper

```python
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects

async with ConfigClient("hostname") as client:
    loads = get_objects(client, type=["Load", "Button"])
```

### Lookup objects by id, using a helper

```python
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects_by_id

async with ConfigClient("hostname") as client:
    objects = get_objects_by_id(client, [118])
```


### Make a request using a method class

```python
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.introspection import GetVersion

async with ConfigClient("hostname") as client:
    version = await client.request(GetVersion)
```


### Make a request using a method class, with params

```python
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.login import Login

async with ConfigClient("hostname") as client:
    await client.request(Login, Login.Params("username", "password"))
```

### Make a raw request

```python
from aiovantage.config_client import ConfigClient

async with ConfigClient("hostname") as client:
    response = await client.raw_request("IIntrospection", "<GetVersion></GetVersion>")

```
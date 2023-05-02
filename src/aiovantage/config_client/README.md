# Vantage InFusion ACI (Application Communication Interface) Service

The ACI service is an XML-based RPC service that Design Center uses to communicate with
Vantage InFusion Controllers. There are a number of interfaces exposed, each with one
or more methods.

The service is exposed on port 2010 (SSL) by default, and on port 2001 (non-SSL) if this
port has been opened by the firewall on the controller.

This client handles making requests to the ACI service, including SSL, authentication,
and XML serializing/deserializing.


## General Usage

You can use the client as follows, for example to run the `IIntrospection.GetVersion`
RPC call:

```python
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.methods.introspection import GetVersion

async with ConfigClient("host", "username", "password") as client:
    response = await client.request(GetVersion)
    print(f"Application version is {response.app}")
```


If you'd prefer not to use the async context manager, just make sure to call `close` yourself:


```python
from aiovantage.config_client import ConfigClient

client = ConfigClient("host", "username", "password")
response = await client.request(Method, Params())
await client.close()
```
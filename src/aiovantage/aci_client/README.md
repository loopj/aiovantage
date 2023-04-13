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
from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.interfaces import IIntrospection
from aiovantage.aci_client.methods.introspection import GetVersion

async with ACIClient("host", "username", "password") as client:
    response = await client.request(IIntrospection, GetVersion)
    print(f"Application version is {response.app}")
```


If you'd prefer not to use the async context manager, just make sure to call `connect`
and `close` yourself:


```python
from aiovantage.aci_client import ACIClient

client = ACIClient("host", "username", "password")
await client.connect()
response = await client.request(Interface, Method, Params())
await client.close()
```
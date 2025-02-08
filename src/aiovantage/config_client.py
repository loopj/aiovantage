"""Client for the Vantage Application Communication Interface (ACI) service.

The ACI service is an XML-based RPC service that Design Center uses to communicate
with Vantage InFusion Controllers. There are a number of "interfaces" exposed, each
with one or more "methods".

This service allows you to query the "configuration" of a Vantage system, for
example fetching a list of all the objects, getting a backup of the Design Center
XML, etc.

The service is exposed on port 2010 (SSL) by default, and on port 2001 (non-SSL) if
this port has been opened by the firewall on the controller.

The service is discoverable via mDNS as `_aci._tcp.local` and/or
`_secure_aci._tcp.local`.
"""

from ._config_client.client import ConfigClient
from ._config_client.interfaces.configuration import ConfigurationInterface
from ._config_client.interfaces.introspection import IntrospectionInterface
from ._config_client.interfaces.login import LoginInterface

__all__ = [
    "ConfigClient",
    "ConfigurationInterface",
    "IntrospectionInterface",
    "LoginInterface",
]

"""Connection to a Vantage ACI server."""

from aiovantage.connection import BaseConnection


class ConfigConnection(BaseConnection):
    """Connection to a Vantage ACI server."""

    default_port = 2001
    default_ssl_port = 2010
    buffer_limit = 2**20

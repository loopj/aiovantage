"""Connection to a Vantage Host Command service."""

from aiovantage.connection import BaseConnection


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010

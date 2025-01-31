"""Connection to a Vantage Host Command service."""

import re

from typing_extensions import override

from aiovantage.connection import BaseConnection
from aiovantage.errors import LoginFailedError


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010

    @property
    def authenticated(self) -> bool:
        """Check if the connection is authenticated."""
        return self._authenticated

    @property
    def requires_authentication(self) -> bool:
        """Check if the connection requires authentication."""
        return self._requires_authentication

    @property
    def supports_enhanced_log(self) -> bool | None:
        """Check if the connection supports enhanced log commands."""
        return self._ellag_state is not None

    @property
    def initial_elagg_state(self) -> bool | None:
        """The initial state of the ELAGG command on the connection."""
        return self._ellag_state

    async def authenticate(self, username: str, password: str) -> None:
        """Authenticate the connection."""
        # Send the login command
        await self.write(f"LOGIN {username} {password}\n")

        # Check for errors
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            raise LoginFailedError(response)

        self._authenticated = True
        self._ellag_state = await self._get_elagg_state()

    @override
    async def _post_open(self) -> None:
        self._authenticated = False
        self._requires_authentication = await self._get_requires_authentication()

        if not self._requires_authentication:
            self._ellag_state = await self._get_elagg_state()

    async def _get_requires_authentication(self) -> bool:
        """Check if the connection requires authentication."""
        if self.authenticated:
            return False

        # Send an ECHO command
        await self.write("ECHO\n")

        # If we get an error, we need to authenticate
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            return True

        return False

    async def _get_elagg_state(self) -> bool | None:
        """Check if the connection supports enhanced log commands."""
        # Send the ELAGG command
        await self.write("ELAGG 1\n")

        # Check the response matches the expected format
        response = await self.readuntil(b"\r\n")
        match = re.search(r"R:ELAGG 1 (ON|OFF)", response)
        if match:
            return match.group(1) == "ON"

        return None

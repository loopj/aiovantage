import re

from typing_extensions import override

from aiovantage._connection import BaseConnection
from aiovantage.errors import ClientConnectionError, LoginFailedError


class ConfigConnection(BaseConnection):
    """Connection to a Vantage ACI server."""

    default_port = 2001
    default_ssl_port = 2010
    buffer_limit = 2**20

    @property
    def authenticated(self) -> bool:
        """Check if the connection is authenticated."""
        if self.closed:
            raise ClientConnectionError("Client not connected")

        return self._authenticated

    @property
    def requires_authentication(self) -> bool:
        """Check if the connection requires authentication."""
        if self.closed:
            raise ClientConnectionError("Client not connected")

        return self._requires_authentication

    async def authenticate(self, username: str, password: str) -> None:
        """Authenticate the connection.

        Args:
            username: The username to use for authentication.
            password: The password to use for authentication.
        """
        if self.closed:
            raise ClientConnectionError("Client not connected")

        # Call the ILogin.Login method
        await self.write(
            f"<ILogin><Login><call><User>{username}</User>"
            f"<Password>{password}</Password></call></Login></ILogin>\n"
        )

        # Fetch the response
        response = await self.readuntil(b"</ILogin>\n")

        # Parse the response
        match = re.search(
            r"<ILogin>\s*<Login>\s*<return>\s*"
            r"(true|false)\s*"
            r"</return>\s*</Login>\s*</ILogin>",
            response,
        )

        if not match:
            raise LoginFailedError("Failed to parse login response")

        if match.group(1) == "false":
            raise LoginFailedError("Invalid username or password")

        self._authenticated = True

    @override
    async def open(self) -> None:
        await super().open()

        self._authenticated = False
        self._requires_authentication = await self._get_requires_authentication()

        # Making unauthorized requests can close the connection, so let's explicitly
        # reopen it if we know we made an unauthorized request
        if self._requires_authentication:
            self.close()
            await super().open()

    async def _get_requires_authentication(self) -> bool:
        if self.authenticated:
            return False

        # Call the IIntrospection.GetSysInfo method
        await self.write(
            "<IIntrospection><GetSysInfo><call></call></GetSysInfo></IIntrospection>\n"
        )

        # Fetch the response
        response = await self.readuntil(b"</IIntrospection>\n")

        # Responses containing the SysInfo element indicate a successful request
        # and therefore no authentication is required
        if re.search(
            r"(?s)<IIntrospection>\s*<GetSysInfo>\s*<return>\s*"
            r"<SysInfo>.*?</SysInfo>\s*"
            r"</return>\s*</GetSysInfo>\s*</IIntrospection>",
            response,
        ):
            return False

        return True

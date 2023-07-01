"""Helper utilities for Vantage controller discovery."""
from dataclasses import dataclass

from aiovantage.command_client.commands import CommandClient
from aiovantage.errors import (
    ClientConnectionError,
    LoginFailedError,
    LoginRequiredError,
)


@dataclass
class DiscoveredVantageController:
    """Model for a discovered Vantage controller."""

    host: str
    supports_ssl: bool
    requires_auth: bool


async def _auth_required(client: CommandClient) -> bool:
    # Check if authentication is required for the given client.
    try:
        await client.command("VERSION")
        return False
    except LoginRequiredError:
        return True


async def discover_controller(host: str) -> DiscoveredVantageController:
    """Discover Vantage controller details from given hostname/ip.

    Args:
        host: The hostname/ip of the Vantage controller.

    Returns:
        A DiscoveredVantageController object.

    Raises:
        ClientConnectionError: If a controller could not be reached.
    """
    try:
        # Try connecting with SSL first
        async with CommandClient(host) as client:
            supports_ssl = True
            requires_auth = await _auth_required(client)
    except ClientConnectionError:
        # If SSL fails, try connecting without SSL
        async with CommandClient(host, ssl=False) as client:
            supports_ssl = False
            requires_auth = await _auth_required(client)

    return DiscoveredVantageController(host, supports_ssl, requires_auth)


async def auth_required(host: str, ssl: bool = True) -> bool:
    """Check if authentication is required for the given controller.

    Args:
        host: The hostname/ip of the Vantage controller.
        ssl: Whether to use SSL when connecting to the controller.

    Returns:
        True if authentication is required, False otherwise.

    Raises:
        ClientConnectionError: If a controller could not be reached.
    """
    async with CommandClient(host, ssl=ssl) as client:
        return await _auth_required(client)


async def valid_credentials(
    host: str, username: str, password: str, ssl: bool = True
) -> bool:
    """Check if the given credentials are valid for the given controller.

    Args:
        host: The hostname/ip of the Vantage controller.
        ssl: Whether to use SSL when connecting to the controller.
        username: The username to check.
        password: The password to check.

    Returns:
        True if the credentials are valid, False otherwise.

    Raises:
        ClientConnectionError: If a controller could not be reached.
    """
    try:
        async with CommandClient(host, username, password, ssl=ssl) as client:
            await client.command("VERSION")
            return True
    except LoginFailedError:
        return False

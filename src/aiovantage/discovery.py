"""Helper utilities for Vantage controller discovery."""
from dataclasses import dataclass

from aiovantage.command_client.commands import CommandClient
from aiovantage.errors import ClientConnectionError, LoginRequiredError


@dataclass
class DiscoveredVantageController:
    """Model for a discovered Vantage controller."""

    host: str
    supports_ssl: bool
    requires_auth: bool


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
            requires_auth = await is_auth_required(client)
    except ClientConnectionError:
        # If SSL fails, try connecting without SSL
        async with CommandClient(host, ssl=False) as client:
            supports_ssl = False
            requires_auth = await is_auth_required(client)

    return DiscoveredVantageController(host, supports_ssl, requires_auth)


async def is_auth_required(client: CommandClient) -> bool:
    """Check if authentication is required for the given client.

    Args:
        client: The CommandClient to check.

    Returns:
        True if authentication is required, False otherwise.
    """
    try:
        await client.command("VERSION")
        return False
    except LoginRequiredError:
        return True

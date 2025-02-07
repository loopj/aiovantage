"""Helper utilities for discovering details about Vantage controllers."""

import re
from dataclasses import dataclass
from ssl import SSLContext

from aiovantage.command_client import CommandClient
from aiovantage.config_client import ConfigClient, IntrospectionInterface
from aiovantage.errors import (
    ClientConnectionError,
    ClientError,
    LoginFailedError,
    LoginRequiredError,
)


@dataclass
class VantageControllerDetails:
    """Details about a queried Vantage controller."""

    host: str
    supports_ssl: bool
    requires_auth: bool


async def get_controller_details(
    host: str, ssl_context: SSLContext | None = None
) -> VantageControllerDetails | None:
    """Discover Vantage controller details from given hostname/ip.

    Args:
        host: The hostname/ip of a Vantage controller.
        ssl_context: Optional SSL context to use when connecting using SSL.

    Returns:
        A DiscoveredVantageController, or None if a controller could not be reached.
    """
    try:
        # Try connecting with SSL first
        async with CommandClient(
            host, ssl=ssl_context if ssl_context else True
        ) as client:
            supports_ssl = True
            requires_auth = await _auth_required(client)
    except ClientConnectionError:
        # If SSL fails, try connecting without SSL
        try:
            async with CommandClient(host, ssl=False) as client:
                supports_ssl = False
                requires_auth = await _auth_required(client)
        except ClientConnectionError:
            # If both fail, the controller is unreachable
            return None

    return VantageControllerDetails(host, supports_ssl, requires_auth)


async def is_auth_required(host: str, *, ssl: SSLContext | bool = True) -> bool:
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


async def validate_credentials(
    host: str, username: str, password: str, *, ssl: SSLContext | bool = True
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


async def get_serial_from_controller(
    host: str,
    username: str | None = None,
    password: str | None = None,
    *,
    ssl: SSLContext | bool = True,
) -> int | None:
    """Get the serial number of the given controller.

    Args:
        host: The hostname/ip of the Vantage controller.
        username: The username to check, or None if not required.
        password: The password to check, or None if not required.
        ssl: Whether to use SSL when connecting to the controller.

    Returns:
        The serial number of the controller, or None if not found.
    """
    try:
        async with ConfigClient(host, username, password, ssl=ssl) as client:
            sys_info = await IntrospectionInterface.get_sys_info(client)
            return sys_info.serial_number

    except ClientError:
        return None


def get_serial_from_hostname(hostname: str) -> str | None:
    """Get the serial number from a Vantage mDNS hostname.

    Args:
        hostname: The hostname to parse.

    Returns:
        The serial number of the controller, or None if not found.
    """
    match = re.match(r"ic-ii-(?P<serial_number>\d+)", hostname)
    if not match:
        return None
    return match.group("serial_number")


async def _auth_required(client: CommandClient) -> bool:
    # Check if authentication is required for the given client.
    try:
        await client.command("VERSION")
        return False
    except LoginRequiredError:
        return True

"""ScenePoint Dual Relay Station."""

from dataclasses import dataclass

from .keypad import Keypad


@dataclass(kw_only=True)
class DualRelayStation(Keypad):
    """ScenePoint Dual Relay Station."""

    shade_controller: bool
    reverse_shade: bool

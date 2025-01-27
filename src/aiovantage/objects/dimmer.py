"""ScenePoint Dimmer Station."""

from dataclasses import dataclass

from .keypad import Keypad


@dataclass(kw_only=True)
class Dimmer(Keypad):
    """ScenePoint Dimmer Station."""

    gang: int
    distributed: bool
    no_neutral: bool = False
    voltage: int | None = None
    alert: str | None = None

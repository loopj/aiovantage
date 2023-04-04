from dataclasses import dataclass
from typing import TypeVar

from typing_extensions import dataclass_transform

T = TypeVar("T")


@dataclass_transform()
def params_dataclass(cls: type[T]) -> type[T]:
    """Add a Meta class to a dataclass, so we can override the name of the root element."""

    class Meta:
        name = "call"

    setattr(cls, "Meta", Meta)
    return dataclass(cls)
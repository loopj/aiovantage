"""LoadGroup object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.load import LoadInterface

from . import LocationObject


@dataclass
class LoadGroup(LocationObject, LoadInterface):
    """LoadGroup object."""

    load_ids: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Load",
            "wrapper": "LoadTable",
        },
    )

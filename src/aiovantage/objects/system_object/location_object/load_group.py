"""LoadGroup object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.load import LoadInterface

from . import LocationObject


@dataclass(kw_only=True)
class LoadGroup(LocationObject, LoadInterface):
    """LoadGroup object."""

    load_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Load",
            "wrapper": "LoadTable",
        },
    )

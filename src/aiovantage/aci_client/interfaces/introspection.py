from dataclasses import dataclass, field
from typing import Optional

from ..methods.introspection.get_version import GetVersion

@dataclass
class IIntrospection:
    get_version: Optional[GetVersion] = field(
        default=None,
        metadata={
            "name": "GetVersion",
            "type": "Element",
        }
    )
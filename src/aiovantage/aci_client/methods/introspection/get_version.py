from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GetVersion:
    call: Optional[object] = None
    return_value: Optional["GetVersion.Return"] = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )

    @dataclass
    class Return:
        kernel: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        rootfs: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        app: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

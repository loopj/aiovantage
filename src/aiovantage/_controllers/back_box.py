from aiovantage.controllers import BaseController
from aiovantage.objects import BackBox


class BackBoxesController(BaseController[BackBox]):
    """Back boxes controller.

    Back boxes typically represent a "gang box" in a wall which may contain
    multiple stations, dimmers, etc. It is mostly useful to know about these
    devices so we can set up a proper device hierarchy.
    """

    vantage_types = ("BackBox",)

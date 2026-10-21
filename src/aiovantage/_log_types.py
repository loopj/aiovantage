"""Types shared by the trigger and system logs, live and historic."""

from enum import IntEnum


class TriggerType(IntEnum):
    """Type of the event that triggered a task, as recorded in the trigger history."""

    BUTTON_UP = 0
    BUTTON_DOWN = 1
    BUTTON_HOLD = 2
    TIMER = 3
    DATA = 4
    POSITION = 5
    IN_RANGE = 6
    OUT_OF_RANGE = 7
    TEMPERATURE = 8
    DAY_MODE = 9
    FAN_MODE = 10
    OPERATION_MODE = 11
    CONNECT = 12
    DISCONNECT = 13
    BOOT = 14
    LEARN = 15
    TAP = 16

    # Observed rather than documented: raised by a module that loses a line feed,
    # with what looks like the feed number in param1
    MODULE_ALERT = 0xA004


class SysLogType(IntEnum):
    """Type of a system log entry.

    In the order of the levels accepted by the Host Command "LOG" command.
    """

    DEBUG = 0
    DUMP = 1
    INFORMATION = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5
    TASK = 6
    DEVICE = 7
    QUERY = 8
    PROF = 9

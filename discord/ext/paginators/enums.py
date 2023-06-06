import enum


__all__ = [
    "StopAction",
    "CodeblockType"
]


class StopAction(enum.Enum):
    DISABLE_VIEW = 0
    REMOVE_VIEW = 1
    EDIT_MESSAGE = 2
    DELETE_MESSAGE = 3


class CodeblockType(enum.Enum):
    NONE = 0
    INLINE = 1
    BLOCK = 2

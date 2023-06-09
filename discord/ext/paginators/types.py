from typing import Any

from discord.ext import commands
from typing_extensions import TypeVar

from .controller import Controller


__all__ = [
    "ContextT",
    "ControllerT",
]


ContextT = TypeVar(
    "ContextT",
    bound=commands.Context[Any],
    default=commands.Context[Any],
)
ControllerT = TypeVar(
    "ControllerT",
    bound=Controller,
    default=Controller,
)

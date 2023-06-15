from collections.abc import Awaitable, Callable
from typing import Any, TYPE_CHECKING, TypeAlias

from discord.ext import commands
from typing_extensions import TypeVar

from .controller import Controller

if TYPE_CHECKING:
    from .paginators.base import BasePaginator


__all__ = [
    "ContextT",
    "ControllerT",
    "Callback",
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

Callback: TypeAlias = Callable[["BasePaginator"], Awaitable[None]]

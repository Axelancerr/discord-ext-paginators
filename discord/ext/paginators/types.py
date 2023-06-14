from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias, TYPE_CHECKING

from discord.ext import commands
from typing_extensions import TypeVar

from .controller import Controller

if TYPE_CHECKING:
    from .paginators.base import BasePaginator


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

Callback: TypeAlias = Callable[["BasePaginator"], Awaitable[None]]

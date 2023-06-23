from collections.abc import Awaitable, Callable
from typing import Any, TYPE_CHECKING, TypeAlias

from discord.ext import commands
from typing_extensions import TypeVar

if TYPE_CHECKING:
    from .controllers import BaseController, DefaultController
    from .paginators import BasePaginator


__all__ = [
    "ContextT",
    "ControllerT",
    "PaginatorT",
    "PaginatorStopCallback",
]


ContextT = TypeVar(
    "ContextT",
    bound=commands.Context[Any],
    default=commands.Context[Any],
    covariant=True,
)
ControllerT = TypeVar(
    "ControllerT",
    bound="BaseController",
    default="DefaultController",
    covariant=True,
)
PaginatorT = TypeVar(
    "PaginatorT",
    bound="BasePaginator",
    default="BasePaginator",
    covariant=True,
)

PaginatorStopCallback: TypeAlias = Callable[[PaginatorT], Awaitable[None]]

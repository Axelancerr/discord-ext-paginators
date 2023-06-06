from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

import discord
from discord.ext import commands
from typing_extensions import TypeVar

from .view import PaginatorView


__all__ = [
    "ContextT",
    "ViewT",
    "ViewCheck",
]


ContextT = TypeVar(
    "ContextT",
    bound=commands.Context[Any],
    default=commands.Context[Any],
)
ViewT = TypeVar(
    "ViewT",
    bound=PaginatorView,
    default=PaginatorView,
)

ViewCheck: TypeAlias = Callable[[discord.Interaction, ContextT], Awaitable[bool]]

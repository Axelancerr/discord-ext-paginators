from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias, TypedDict

import discord
from discord.ext import commands
from typing_extensions import TypeVar

from .view import FirstPageButton, LabelButton, LastPageButton, NextPageButton, PreviousPageButton, StopButton


__all__ = [
    "ContextT",
    "ViewCheck",
    "ViewButtons",
]


ContextT = TypeVar(
    "ContextT",
    bound=commands.Context[Any],
    default=commands.Context[Any],
)


ViewCheck: TypeAlias = Callable[[discord.Interaction, ContextT], Awaitable[bool]]


class ViewButtons(TypedDict):
    first: type[FirstPageButton]
    previous: type[PreviousPageButton]
    label: type[LabelButton]
    next: type[NextPageButton]
    last: type[LastPageButton]
    stop: type[StopButton]

import abc
from typing import Generic

import discord

from ..types import PaginatorT


__all__ = ["BaseController"]


class BaseController(discord.ui.View, abc.ABC, Generic[PaginatorT]):

    def __init__(self, paginator: PaginatorT) -> None:
        super().__init__(timeout=paginator.timeout)
        self.paginator: PaginatorT = paginator

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.paginator.ctx.author.id == interaction.user.id

    async def on_timeout(self) -> None:
        await self.paginator.stop(callback=self.paginator.on_timeout)

    @abc.abstractmethod
    def update_item_states(self) -> None:
        raise NotImplementedError

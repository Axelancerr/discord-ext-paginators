import abc
import contextlib
from collections.abc import Sequence
from typing import Any

import discord

from .enums import StopAction
from .view import PaginatorView
from .types import ContextT, ViewT, ViewCheck


__all__ = ["Paginator"]


class Paginator(abc.ABC):

    def __init__(
        self,
        *,
        # paginator
        ctx: ContextT,
        # pages
        items: Sequence[Any],
        items_per_page: int,
        join_items: bool = True,
        join_items_with: str = "\n",
        initial_page: int = 0,
        # view
        view: type[ViewT] = PaginatorView,
        view_timeout: int = 300,
        view_check: ViewCheck | None = None
    ) -> None:
        # paginator
        self.ctx: ContextT = ctx
        # pages
        if join_items is True:
            self.pages: Sequence[Any] = [
                join_items_with.join(items[chunk:chunk + items_per_page])
                for chunk in range(0, len(items), items_per_page)
            ]
        else:
            self.pages: Sequence[Any] = [
                items[chunk:chunk + items_per_page]
                for chunk in range(0, len(items), items_per_page)
            ]
        self.page: int = initial_page
        # message
        self._view_cls: type[ViewT] = view
        self._view_timeout: int = view_timeout
        self._view_check: ViewCheck | None = view_check
        # message
        self.message: discord.Message | None = None
        self.view: PaginatorView | None = None
        self.content: str = discord.utils.MISSING
        self.embeds: list[discord.Embed] = discord.utils.MISSING

    async def start(self) -> None:
        if self.message is not None:
            return
        # set initial states
        self.view = self._view_cls(timeout=self._view_timeout)
        self.view._update_button_states()
        await self._update_page_content()
        # send initial message
        self.message = await self.ctx.reply(
            content=self.content,
            embeds=self.embeds,
            view=self.view
        )

    async def change_page(self, page: int) -> None:
        if self.message is None:
            return
        # set new states
        self.page = page
        self.view._update_button_states()
        await self._update_page_content()
        # edit message
        with contextlib.suppress(discord.NotFound, discord.HTTPException):
            await self.message.edit(  # type: ignore
                content=self.content,
                embeds=self.embeds,
                view=self.view
            )

    async def stop(self, by_timeout: bool = False) -> None:
        if not self.message:
            return
        # enact stop actions
        with contextlib.suppress(discord.NotFound, discord.HTTPException):
            match self.timeout_action if by_timeout else self.stop_action:
                case StopAction.DISABLE_VIEW:
                    for button in self.view.buttons.values():
                        button.disabled = True
                    await self.message.edit(view=self.view)
                case StopAction.REMOVE_VIEW:
                    await self.message.edit(view=None)
                case StopAction.EDIT_MESSAGE:
                    await self.message.edit(  # type: ignore
                        content="*This message has expired*",
                        embeds=[],
                        view=None
                    )
                case StopAction.DELETE_MESSAGE:
                    await self.message.delete()
        # reset variables
        self.message = None
        self.view.stop()
        self.view = discord.utils.MISSING

    @abc.abstractmethod
    async def _update_page_content(self) -> None:
        raise NotImplementedError

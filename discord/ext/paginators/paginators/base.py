import abc
import contextlib
from collections.abc import Sequence
from typing import Any

import discord

from ..callbacks import disable_view, remove_view
from ..controller import Controller
from ..types import Callback, ContextT, ControllerT


__all__ = ["BasePaginator"]


class BasePaginator(abc.ABC):

    def __init__(
        self,
        *,
        # context
        ctx: ContextT,
        # pages
        items: Sequence[Any],
        items_per_page: int,
        join_items: bool = True,
        join_items_with: str = "\n",
        # page
        initial_page: int = 1,
        # settings
        controller: type[ControllerT] = Controller,
        timeout: float = 300.0,
        on_timeout: Callback = disable_view,
        on_stop_button_press: Callback = remove_view,
    ) -> None:
        # context
        self.ctx: ContextT = ctx
        # pages
        if items_per_page <= 0:
            raise ValueError("'items_per_page' must be greater than 0.")
        self.items_per_page = items_per_page
        self.pages: Sequence[Any] = [
            join_items_with.join(items[x:x + items_per_page]) if join_items else items[x:x + items_per_page]
            for x in range(0, len(items), items_per_page)
        ]
        # page
        if initial_page <= 0 or initial_page > len(self.pages):
            raise ValueError(f"'initial_page' must be between 1 and {len(self.pages)} (inclusive).")
        self.page: int = initial_page
        # settings
        self.controller: type[ControllerT] = controller
        self.timeout: float = timeout
        self.on_timeout: Callback = on_timeout
        self.on_stop_button_press: Callback = on_stop_button_press

        # message
        self.message: discord.Message | None = None
        self.view: ControllerT = discord.utils.MISSING
        self.content: str | None = None
        self.embeds: list[discord.Embed] = []

    # methods

    async def start(self) -> None:
        if self.message is not None:
            return
        #
        self.view = self.controller(self)
        self.view.set_button_states()
        await self.set_page_content()
        #
        self.message = await self.ctx.reply(
            content=self.content, embeds=self.embeds,
            view=self.view
        )

    async def change_page(self, page: int) -> None:
        if self.message is None:
            return
        # check if page is valid
        if page <= 0 or page > len(self.pages):
            raise ValueError(f"'page' must be between 1 and {len(self.pages)} (inclusive).")
        self.page = page
        # set new controller state + page contents
        self.view.set_button_states()
        await self.set_page_content()
        # edit message
        with contextlib.suppress(discord.NotFound, discord.HTTPException):
            await self.message.edit(
                content=self.content, embeds=self.embeds,
                view=self.view
            )

    async def stop(self, by_timeout: bool = False) -> None:
        if self.message is None:
            return
        # enact stop actions
        if by_timeout:
            await self.on_timeout(self)
        else:
            await self.on_stop_button_press(self)
        self.view.stop()
        # reset variables
        self.message = None
        self.view = discord.utils.MISSING

    # shortcuts

    async def go_to_first_page(self) -> None:
        await self.change_page(1)

    async def go_to_previous_page(self) -> None:
        await self.change_page(self.page - 1)

    async def go_to_next_page(self) -> None:
        await self.change_page(self.page + 1)

    async def go_to_last_page(self) -> None:
        await self.change_page(len(self.pages))

    # abc methods

    @abc.abstractmethod
    async def set_page_content(self) -> None:
        raise NotImplementedError

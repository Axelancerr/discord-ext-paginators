import abc
import contextlib
from collections.abc import Sequence
from typing import Any

import discord

from .enums import StopAction
from .controller import Controller
from .types import ContextT, ControllerT


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
        initial_page: int = 1,
        # controller
        controller: type[ControllerT] = Controller,
        controller_stop_button_action: StopAction = StopAction.REMOVE_VIEW,
        # timeout
        timeout: float = 300.0,
        timeout_action: StopAction = StopAction.DISABLE_VIEW,
    ) -> None:
        # context
        self.ctx: ContextT = ctx
        # pages
        if items_per_page <= 0:
            raise ValueError("'items_per_page' must be greater than 0.")
        if join_items is True:
            self.pages: Sequence[Any] = [
                join_items_with.join(items[x:x + items_per_page])
                for x in range(0, len(items), items_per_page)
            ]
        else:
            self.pages: Sequence[Any] = [
                items[x:x + items_per_page]
                for x in range(0, len(items), items_per_page)
            ]
        if initial_page <= 0 or initial_page > len(self.pages):
            raise ValueError(f"'initial_page' must be between 1 and {len(self.pages)} (inclusive).")
        self.page: int = initial_page
        # controller
        self.controller: type[ControllerT] = controller
        self.controller_stop_button_action: StopAction = controller_stop_button_action
        # timeout
        self.timeout: float = timeout
        self.timeout_action: StopAction = timeout_action
        # message
        self.message: discord.Message | None = None
        self.view: Controller = discord.utils.MISSING
        self.content: str = discord.utils.MISSING
        self.embeds: list[discord.Embed] = discord.utils.MISSING

    # methods

    async def start(self) -> None:
        if self.message is not None:
            return
        # set initial states
        self.view = self.controller(self)
        self.view.set_button_states()
        await self.set_page_content()
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
        self.view.set_button_states()
        await self.set_page_content()
        # edit message
        with contextlib.suppress(discord.NotFound, discord.HTTPException):
            await self.message.edit(  # type: ignore
                content=self.content,
                embeds=self.embeds,
                view=self.view
            )

    async def stop(self, by_timeout: bool = False) -> None:
        if self.message is None:
            return
        # enact stop actions
        with contextlib.suppress(discord.NotFound, discord.HTTPException):
            match self.timeout_action if by_timeout else self.controller_stop_button_action:
                case StopAction.DISABLE_VIEW:
                    for button in self.view.buttons.values():
                        button.disabled = True
                    await self.message.edit(view=self.view)
                case StopAction.REMOVE_VIEW:
                    await self.message.edit(view=None)
                case StopAction.EDIT_MESSAGE:
                    await self.message.edit(  # type: ignore
                        content="*This message has expired*", embeds=[],
                        view=None
                    )
                case StopAction.DELETE_MESSAGE:
                    await self.message.delete()
        # reset variables
        self.message = None
        self.view.stop()
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

from collections.abc import Sequence

import discord

from .base import BasePaginator
from ..callbacks import disable_view, remove_view
from ..controllers import DefaultController
from ..types import PaginatorStopCallback, ContextT, ControllerT


__all__ = ["EmbedsPaginator"]


class EmbedsPaginator(BasePaginator[ContextT, ControllerT]):

    def __init__(
        self,
        *,
        # context
        ctx: ContextT,
        # pages
        embeds: Sequence[discord.Embed],
        embeds_per_page: int,
        # page
        initial_page: int = 1,
        # settings
        controller: type[ControllerT] = DefaultController,
        timeout: float = 300.0,
        on_timeout: PaginatorStopCallback = disable_view,
        on_stop_button_press: PaginatorStopCallback = remove_view,
    ) -> None:
        if embeds_per_page > 10:
            raise ValueError("'embeds_per_page' must be less than or equal to 10.")
        super().__init__(
            ctx=ctx,
            items=embeds,
            items_per_page=embeds_per_page,
            join_items=False,
            initial_page=initial_page,
            controller=controller,
            timeout=timeout,
            on_timeout=on_timeout,
            on_stop_button_press=on_stop_button_press,
        )

    async def update_page_content(self) -> None:
        self.embeds = self.pages[self.page - 1]

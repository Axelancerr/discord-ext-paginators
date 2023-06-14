from collections.abc import Sequence

import discord

from .base import BasePaginator
from ..callbacks import disable_view, remove_view
from ..controller import Controller
from ..types import Callback, ContextT, ControllerT


__all__ = ["EmbedFieldsPaginator"]


class EmbedFieldsPaginator(BasePaginator):

    def __init__(
        self,
        *,
        # context
        ctx: ContextT,
        # pages
        fields: Sequence[tuple[str, str, bool]],
        fields_per_page: int,
        # page
        initial_page: int = 1,
        # settings
        controller: type[ControllerT] = Controller,
        timeout: float = 300.0,
        on_timeout: Callback = disable_view,
        on_stop_button_press: Callback = remove_view,
        # fields paginator specific
        embed: discord.Embed,
    ) -> None:
        if fields_per_page > 25:
            raise ValueError("'fields_per_page' must be less than or equal to 25.")
        super().__init__(
            ctx=ctx,
            items=fields,
            items_per_page=fields_per_page,
            join_items=False,
            initial_page=initial_page,
            controller=controller,
            timeout=timeout,
            on_timeout=on_timeout,
            on_stop_button_press=on_stop_button_press,
        )
        self.embeds = [embed]

    async def set_page_content(self) -> None:
        self.embeds[0].clear_fields()
        for name, value, inline in self.pages[self.page - 1]:
            self.embeds[0].add_field(name=name, value=value, inline=inline)

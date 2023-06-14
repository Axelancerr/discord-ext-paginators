from collections.abc import Sequence

import discord

from .base import BasePaginator
from ..callbacks import disable_view, remove_view
from ..codeblocks import CodeblockType, codeblock
from ..controller import Controller
from ..types import Callback, ContextT, ControllerT


__all__ = ["EmbedTextPaginator"]


class EmbedTextPaginator(BasePaginator):

    def __init__(
        self,
        *,
        # context
        ctx: ContextT,
        # pages
        items: Sequence[str],
        items_per_page: int,
        join_items_with: str = "\n",
        # page
        initial_page: int = 1,
        # settings
        controller: type[ControllerT] = Controller,
        timeout: float = 300.0,
        on_timeout: Callback = disable_view,
        on_stop_button_press: Callback = remove_view,
        # text paginator
        codeblock_type: CodeblockType = CodeblockType.NONE,
        codeblock_language: str | None = None,
        header: str | None = None,
        footer: str | None = None,
        # embed paginator
        embed: discord.Embed
    ) -> None:
        super().__init__(
            ctx=ctx,
            items=items,
            items_per_page=items_per_page,
            join_items=True,
            join_items_with=join_items_with,
            initial_page=initial_page,
            controller=controller,
            timeout=timeout,
            on_timeout=on_timeout,
            on_stop_button_press=on_stop_button_press,
        )
        self.header: str = header or ""
        self.footer: str = footer or ""
        self.codeblock_start, self.codeblock_end = codeblock(codeblock_type, language=codeblock_language)
        self.embeds = [embed]

    async def set_page_content(self) -> None:
        self.embeds[0].description = f"{self.codeblock_start}" \
                                     f"{self.header}\n" \
                                     f"{self.pages[self.page - 1]}" \
                                     f"\n{self.footer}" \
                                     f"{self.codeblock_end}"

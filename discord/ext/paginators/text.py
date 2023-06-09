from collections.abc import Sequence
from typing import Any

from .base import BasePaginator
from .controller import Controller
from .enums import CodeblockType, StopAction
from .types import ContextT, ControllerT


__all__ = ["TextPaginator"]


class TextPaginator(BasePaginator):

    def __init__(
        self,
        *,
        # context
        ctx: ContextT,
        # pages
        items: Sequence[Any],
        items_per_page: int,
        join_items_with: str = "\n",
        initial_page: int = 0,
        # controller
        controller: type[ControllerT] = Controller,
        controller_stop_button_action: StopAction = StopAction.REMOVE_VIEW,
        # timeout
        timeout: float = 300.0,
        timeout_action: StopAction = StopAction.DISABLE_VIEW,
        # text paginator specific
        codeblock_type: CodeblockType = CodeblockType.NONE,
        codeblock_language: str | None = None,
        header: str | None = None,
        footer: str | None = None,
    ) -> None:
        super().__init__(
            ctx=ctx,
            items=items,
            items_per_page=items_per_page,
            join_items=True,
            join_items_with=join_items_with,
            initial_page=initial_page,
            controller=controller,
            controller_stop_button_action=controller_stop_button_action,
            timeout=timeout,
            timeout_action=timeout_action,
        )
        self.header: str = header or ""
        self.footer: str = footer or ""
        match codeblock_type:
            case CodeblockType.NONE:
                self.codeblock_start = ""
                self.codeblock_end = ""
            case CodeblockType.INLINE:
                self.codeblock_start = "`"
                self.codeblock_end = "`"
            case CodeblockType.BLOCK:
                self.codeblock_start = f"```{codeblock_language}\n"
                self.codeblock_end = "\n```"

    async def set_page_content(self) -> None:
        self.content = f"{self.codeblock_start}{self.header}{self.pages[self.page]}{self.footer}{self.codeblock_end}"

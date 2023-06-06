from collections.abc import Sequence
from typing import Any

from .base import Paginator
from .enums import CodeblockType, StopAction
from .types import ContextT, InteractionCheck


__all__ = ["TextPaginator"]


class TextPaginator(Paginator):

    def __init__(
        self,
        *,
        ctx: ContextT,
        timeout: int | None = 300,
        interaction_check: InteractionCheck | None = None,
        # entries
        entries: Sequence[Any],
        joiner: str = "\n",
        # pages
        per_page: int,
        initial_page: int = 0,
        # actions
        timeout_action: StopAction = StopAction.DISABLE_VIEW,
        stop_action: StopAction = StopAction.DISABLE_VIEW,
        # text paginator specific
        codeblock_type: CodeblockType = CodeblockType.NONE,
        codeblock_language: str | None = None,
        header: str | None = None,
        footer: str | None = None,
    ) -> None:
        super().__init__(
            ctx=ctx,
            timeout=timeout,
            interaction_check=interaction_check,
            entries=entries,
            joiner=joiner,
            per_page=per_page,
            initial_page=initial_page,
            timeout_action=timeout_action,
            stop_action=stop_action,
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

    async def _update_page_content(self) -> None:
        self.content = f"{self.codeblock_start}{self.header}{self.pages[self.page]}{self.footer}{self.codeblock_end}"

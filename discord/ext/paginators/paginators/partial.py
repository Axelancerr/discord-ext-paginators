from collections.abc import Sequence
from typing import Any

from .base import BasePaginator
from ..callbacks import disable_view, remove_view
from ..controllers import DefaultController
from ..types import PaginatorStopCallback, ContextT, ControllerT


__all__ = ["PartialPaginator"]


class PartialPaginator(BasePaginator[ContextT, ControllerT]):

    def __init__(
        self,
        *,
        # pages
        partials: Sequence[Any],
        # page
        initial_page: int = 1,
        # context
        ctx: ContextT,
        # settings
        controller: type[ControllerT] = DefaultController,
        timeout: float = 300.0,
        on_timeout: PaginatorStopCallback = disable_view,
        on_stop_button_press: PaginatorStopCallback = remove_view,
        # partial paginator
        header: str | None = None,
    ) -> None:
        super().__init__(
            ctx=ctx,
            items=partials,
            items_per_page=1,
            join_items=False,
            initial_page=initial_page,
            controller=controller,
            timeout=timeout,
            on_timeout=on_timeout,
            on_stop_button_press=on_stop_button_press,
        )
        self.header: str = header or ""
        self._cache: dict[int, str] = {}

    async def update_page_content(self) -> None:
        page = self.page - 1
        if page not in self._cache:
            async with self.ctx.typing():
                self._cache[page] = await self.pages[page][0]()
        self.content = f"{self.header}{self._cache[page]}"

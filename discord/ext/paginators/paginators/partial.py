from collections.abc import Sequence
from typing import Generic

from typing_extensions import TypeVar

from .base import BasePaginator
from ..callbacks import disable_view, remove_view
from ..controller import Controller
from ..types import Callback, ContextT, ControllerT


__all__ = ["PartialPaginator"]

PartialT = TypeVar("PartialT")


class PartialPaginator(BasePaginator, Generic[PartialT]):

    def __init__(
        self,
        *,
        # context
        ctx: ContextT,
        # pages
        partials: Sequence[PartialT],
        # page
        initial_page: int = 1,
        # settings
        controller: type[ControllerT] = Controller,
        timeout: float = 300.0,
        on_timeout: Callback = disable_view,
        on_stop_button_press: Callback = remove_view,
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

    async def set_page_content(self) -> None:
        page = self.page - 1
        if page not in self._cache:
            async with self.ctx.typing():
                self._cache[page] = await self.pages[page][0]()
        self.content = f"{self.header}{self._cache[page]}"

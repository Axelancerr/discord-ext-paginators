from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .paginators.base import BasePaginator


__all__ = [
    "disable_view",
    "remove_view",
    "edit_message",
    "delete_message",
]


async def disable_view(paginator: BasePaginator) -> None:
    for button in paginator.view.buttons.values():
        button.disabled = True
    assert paginator.message is not None
    await paginator.message.edit(view=paginator.view)


async def remove_view(paginator: BasePaginator) -> None:
    assert paginator.message is not None
    await paginator.message.edit(view=None)


async def edit_message(paginator: BasePaginator) -> None:
    assert paginator.message is not None
    await paginator.message.edit(view=None, content="*paginator stopped*", embeds=[])


async def delete_message(paginator: BasePaginator) -> None:
    assert paginator.message is not None
    await paginator.message.delete()

from .base import BaseController
from .buttons import FirstPageButton, LabelButton, LastPageButton, NextPageButton, PreviousPageButton, StopButton
from ..types import PaginatorT


__all__ = ["DefaultController"]


class DefaultController(BaseController[PaginatorT]):

    def __init__(self, paginator: PaginatorT) -> None:
        super().__init__(paginator)
        if len(self.paginator.pages) == 1:
            self.items = {
                "label": LabelButton(label="?"),
                "stop":  StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
            }
        elif len(self.paginator.pages) == 2:
            self.items = {
                "previous": PreviousPageButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                "label":    LabelButton(label="?"),
                "next":     NextPageButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
            }
        else:
            self.items = {
                "first":    FirstPageButton(emoji="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}"),
                "previous": PreviousPageButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                "label":    LabelButton(label="?"),
                "next":     NextPageButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                "last":     LastPageButton(emoji="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}"),
                "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
            }
        for item in self.items.values():
            self.add_item(item)

    def update_item_states(self) -> None:
        self.items["label"].label = f"{self.paginator.page}/{len(self.paginator.pages)}"
        if "first" in self.items:
            self.items["first"].disabled = self.paginator.page <= 2
            self.items["last"].disabled = self.paginator.page >= len(self.paginator.pages) - 1
        if "previous" in self.items:
            self.items["previous"].disabled = self.paginator.page <= 1
            self.items["next"].disabled = self.paginator.page >= len(self.paginator.pages)

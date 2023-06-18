from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from .paginators.base import BasePaginator


__all__ = [
    "ControllerButton",
    "FirstPageButton",
    "PreviousPageButton",
    "LabelButton",
    "NextPageButton",
    "LastPageButton",
    "StopButton",
    "Controller",
]


class ControllerButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()


class FirstPageButton(ControllerButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        await self.view.paginator.go_to_first_page()  # pyright: ignore


class PreviousPageButton(ControllerButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        await self.view.paginator.go_to_previous_page()  # pyright: ignore


class LabelButton(ControllerButton):
    pass


class NextPageButton(ControllerButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        await self.view.paginator.go_to_next_page()  # pyright: ignore


class LastPageButton(ControllerButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        await self.view.paginator.go_to_last_page()  # pyright: ignore


class StopButton(ControllerButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        await self.view.paginator.stop()  # pyright: ignore


class Controller(discord.ui.View):

    def __init__(self, paginator: BasePaginator) -> None:
        super().__init__(timeout=paginator.timeout)
        self.paginator: BasePaginator = paginator
        match len(self.paginator.pages):
            case 1:
                self.items = {
                    "label": LabelButton(label="?"),
                    "stop":  StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
            case 2:
                self.items = {
                    "previous": PreviousPageButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                    "label":    LabelButton(label="?"),
                    "next":     NextPageButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                    "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
            case _:
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.paginator.ctx.author.id

    async def on_timeout(self) -> None:
        await self.paginator.stop(by_timeout=True)

    def set_button_states(self) -> None:
        self.items["label"].label = f"{self.paginator.page}/{len(self.paginator.pages)}"
        if "first" in self.items:
            self.items["first"].disabled = self.paginator.page <= 2
            self.items["last"].disabled = self.paginator.page >= len(self.paginator.pages) - 1
        if "previous" in self.items:
            self.items["previous"].disabled = self.paginator.page <= 1
            self.items["next"].disabled = self.paginator.page >= len(self.paginator.pages)

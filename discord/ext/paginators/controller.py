from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from .paginators.base import BasePaginator


__all__ = ["Controller"]


class FirstPageButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_first_page()  # pyright: ignore


class PreviousPageButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_previous_page()  # pyright: ignore


class LabelButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()


class NextPageButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_next_page()  # pyright: ignore


class LastPageButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_last_page()  # pyright: ignore


class StopButton(discord.ui.Button["Controller"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.stop()  # pyright: ignore


class Controller(discord.ui.View):

    def __init__(self, paginator: BasePaginator) -> None:
        super().__init__(timeout=paginator.timeout)
        self.paginator: BasePaginator = paginator
        match len(self.paginator.pages):
            case 1:
                self.buttons = {
                    "label": LabelButton(label="?"),
                    "stop":  StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
            case 2:
                self.buttons = {
                    "previous": PreviousPageButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                    "label":    LabelButton(label="?"),
                    "next":     NextPageButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                    "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
            case _:
                self.buttons = {
                    "first":    FirstPageButton(emoji="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}"),
                    "previous": PreviousPageButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                    "label":    LabelButton(label="?"),
                    "next":     NextPageButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                    "last":     LastPageButton(emoji="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}"),
                    "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
        for button in self.buttons.values():
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.paginator.ctx.author.id

    async def on_timeout(self) -> None:
        await self.paginator.stop(by_timeout=True)

    def set_button_states(self) -> None:
        self.buttons["label"].label = f"{self.paginator.page}/{len(self.paginator.pages)}"
        if "first" in self.buttons:
            self.buttons["first"].disabled = self.paginator.page <= 2
            self.buttons["last"].disabled = self.paginator.page >= len(self.paginator.pages) - 1
        if "previous" in self.buttons:
            self.buttons["previous"].disabled = self.paginator.page <= 1
            self.buttons["next"].disabled = self.paginator.page >= len(self.paginator.pages)

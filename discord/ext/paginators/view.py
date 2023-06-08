from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from .base import Paginator
    from .types import ViewButtons


__all__ = [
    "FirstPageButton",
    "PreviousPageButton",
    "LabelButton",
    "NextPageButton",
    "LastPageButton",
    "StopButton",
    "View"
]


class FirstPageButton(discord.ui.Button["View"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        # pycharm doesn't understand descriptors
        await interaction.response.defer()
        await self.view.paginator.go_to_first_page()  # pyright: ignore


class PreviousPageButton(discord.ui.Button["View"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_previous_page()  # pyright: ignore


class LabelButton(discord.ui.Button["View"]):
    pass


class NextPageButton(discord.ui.Button["View"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_next_page()  # pyright: ignore


class LastPageButton(discord.ui.Button["View"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.go_to_last_page()  # pyright: ignore


class StopButton(discord.ui.Button["View"]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        await self.view.paginator.stop()  # pyright: ignore


VIEW_BUTTONS: ViewButtons = {
    "first":    FirstPageButton,
    "previous": PreviousPageButton,
    "label":    LabelButton,
    "next":     NextPageButton,
    "last":     LastPageButton,
    "stop":     StopButton
}


class View(discord.ui.View):

    def __init__(self, paginator: Paginator) -> None:
        super().__init__(
            timeout=paginator.view_timeout
        )
        self.paginator: Paginator = paginator
        match len(self.paginator.pages):
            case 1:
                self.buttons = {
                    "label": self.paginator.view_buttons["label"](),
                    "stop":  self.paginator.view_buttons["stop"]()
                }
            case 2:
                self.buttons = {
                    "previous": self.paginator.view_buttons["previous"](),
                    "label":    self.paginator.view_buttons["label"](),
                    "next":     self.paginator.view_buttons["next"](),
                    "stop":     self.paginator.view_buttons["stop"]()
                }
            case _:
                self.buttons = {
                    "first":    self.paginator.view_buttons["first"](),
                    "previous": self.paginator.view_buttons["previous"](),
                    "label":    self.paginator.view_buttons["label"](),
                    "next":     self.paginator.view_buttons["next"](),
                    "last":     self.paginator.view_buttons["last"](),
                    "stop":     self.paginator.view_buttons["stop"]()
                }
        for button in self.buttons.values():
            self.add_item(button)


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.paginator.view_check is not None:
            return await self.paginator.view_check(interaction, self.paginator.ctx)
        return interaction.user.id == self.paginator.ctx.author.id

    async def on_timeout(self) -> None:
        await self.paginator.stop(by_timeout=True)

    def _update_button_states(self) -> None:
        # enable or disable the first and previous buttons
        on_first_page = (self.paginator.page == 0)
        self.buttons["first"].disabled = on_first_page
        self.buttons["previous"].disabled = on_first_page
        # update the label button to show the current page
        self.buttons["label"].label = f"{self.paginator.page + 1}/{len(self.paginator.pages)}"
        # enable or disable the next and last buttons
        on_last_page = (self.paginator.page == len(self.paginator.pages) - 1)
        self.buttons["next"].disabled = on_last_page
        self.buttons["last"].disabled = on_last_page

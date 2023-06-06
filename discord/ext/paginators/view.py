from __future__ import annotations

from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from .base import Paginator


__all__ = ["PaginatorView"]


class BaseButton(discord.ui.Button["PaginatorView"]):

    @property
    def view(self) -> PaginatorView:
        # buttons are added to the view before it is sent, so this should never be None.
        return self._view  # pyright: ignore

    @property
    def paginator(self) -> Paginator:
        return self.view.paginator


class FirstButton(BaseButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.paginator.change_page(0)


class PreviousButton(BaseButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.paginator.change_page(self.paginator.page - 1)


class LabelButton(BaseButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()


class NextButton(BaseButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.paginator.change_page(self.paginator.page + 1)


class LastButton(BaseButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.paginator.change_page(len(self.paginator.pages) - 1)


class StopButton(BaseButton):

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.paginator.stop()


class PaginatorView(discord.ui.View):

    def __init__(self, paginator: Paginator) -> None:
        self.paginator: Paginator = paginator
        match len(self.paginator.pages):
            case 1:
                self.buttons = {
                    "label": LabelButton(label="0/0"),
                    "stop":  StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
            case 2:
                self.buttons = {
                    "previous": PreviousButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                    "label":    LabelButton(label="0/0"),
                    "next":     NextButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                    "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
            case _:
                self.buttons = {
                    "first":    FirstButton(emoji="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}"),
                    "previous": PreviousButton(emoji="\N{BLACK LEFT-POINTING TRIANGLE}"),
                    "label":    LabelButton(label="0/0"),
                    "next":     NextButton(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}"),
                    "last":     LastButton(emoji="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}"),
                    "stop":     StopButton(emoji="\N{BLACK SQUARE FOR STOP}")
                }
        for button in self.buttons.values():
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.paginator._view_check is not None:
            return await self.paginator._view_check(interaction, self.paginator.ctx)
        return interaction.user.id == self.paginator.ctx.author.id

    async def on_timeout(self) -> None:
        await self.paginator.stop(by_timeout=True)

    def _update_button_states(self) -> None:
        # update the label button to show the current page
        self.buttons["label"].label = f"{self.paginator.page + 1}/{len(self.paginator.pages)}"
        # enable or disable the first and previous buttons
        on_first_page = (self.paginator.page == 0)
        self.buttons["first"].disabled = on_first_page
        self.buttons["previous"].disabled = on_first_page
        # enable or disable the next and last buttons
        on_last_page = (self.paginator.page == len(self.paginator.pages) - 1)
        self.buttons["next"].disabled = on_last_page
        self.buttons["last"].disabled = on_last_page

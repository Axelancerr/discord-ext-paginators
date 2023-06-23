import discord

from ..types import ControllerT


__all__ = [
    "FirstPageButton",
    "PreviousPageButton",
    "LabelButton",
    "NextPageButton",
    "LastPageButton",
    "StopButton",
]


class BaseButton(discord.ui.Button[ControllerT]):

    async def callback(self, interaction: discord.Interaction) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()


class FirstPageButton(BaseButton[ControllerT]):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        assert self.view is not None
        await self.view.paginator.go_to_first_page()


class PreviousPageButton(BaseButton[ControllerT]):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        assert self.view is not None
        await self.view.paginator.go_to_previous_page()


class LabelButton(BaseButton[ControllerT]):
    pass


class NextPageButton(BaseButton[ControllerT]):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        assert self.view is not None
        await self.view.paginator.go_to_next_page()


class LastPageButton(BaseButton[ControllerT]):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        assert self.view is not None
        await self.view.paginator.go_to_last_page()


class StopButton(BaseButton[ControllerT]):

    async def callback(self, interaction: discord.Interaction) -> None:
        await super().callback(interaction)
        assert self.view is not None
        await self.view.paginator.stop(callback=self.view.paginator.on_stop_button_press)

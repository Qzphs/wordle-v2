"""
Hideout v0.2

Support for private discord bot used with friends.

https://github.com/Qzphs/hideout
"""

__all__ = [
    "bot",
    "command",
    "event",
    "Function",
    "function",
    "Interaction",
    "Message",
    "on_quit",
    "SlashCommand",
    "whitelist",
]


import argparse
import functools
import json
from typing import Awaitable, Callable

import discord
from discord.ext import commands


class Config:

    def __init__(self):
        with open("bot.json") as file:
            config = json.load(file)
        self.channel_id: int = config["channel"]
        self.__token: str = config["token"]
        self.whitelist: list[int] = config["whitelist"]

    @property
    def token(self):
        token = self.__token
        self.__token = ""
        return token


config = Config()
whitelist: list[discord.User] = []


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=[])

    async def on_ready(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--sync", action="store_true")
        args = vars(parser.parse_args())
        if args["sync"]:
            await self.tree.sync()

        for user_id in config.whitelist:
            whitelist.append(await self.fetch_user(user_id))

        self.channel = await self.fetch_channel(config.channel_id)
        await self.on_ready_hook()

    async def on_ready_hook(self):
        pass

    def run(self):
        super().run(config.token)


bot = Bot()
command = bot.tree.command


def event(func: Callable[[], Awaitable[None]]):
    if func.__name__ == "on_ready":
        bot.on_ready_hook = func
    else:
        bot.event(func)


class Interaction:
    """
    Provide a uniform interface for responding to users.

    The bot could respond to either a normal message sent in a channel
    or a slash command. The callback function should instantiate a
    subclass and send messages through that instance.
    """

    @property
    def channel(self) -> discord.TextChannel:
        raise NotImplementedError

    @property
    def user(self) -> discord.User:
        raise NotImplementedError

    async def reply(self, text: str):
        raise NotImplementedError


class Message(Interaction):
    """Interaction subclass for responding to normal messages."""

    def __init__(self, message: discord.Message):
        super().__init__()
        self.message = message

    @property
    def channel(self):
        return self.message.channel

    @property
    def user(self):
        return self.message.author

    async def reply(self, text: str):
        await self.message.channel.send(text)


class SlashCommand(Interaction):
    """Interaction subclass for responding to slash commands."""

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    @property
    def channel(self):
        return self.interaction.channel

    @property
    def user(self):
        return self.interaction.user

    async def reply(self, text: str):
        await self.interaction.response.send_message(text)


Function = Callable[..., Awaitable[None]]


def function(callback: Function):
    """
    Decorator for hideout functions.

    Hideout functions are intended to be called by actual Discord
    commands. (This is a workaround to issues with wrapping commands
    directly when they have parameters.)

    Hideout functions can only be used by whitelisted users. This
    decorator also catches any errors raised by the function and sends
    the error message to the user.
    """

    @functools.wraps(callback)
    async def wrapper(interaction: Interaction, *args, **kwargs):
        try:
            if interaction.user not in whitelist:
                await interaction.reply(
                    "You can't use commands. (Ask to be added to the whitelist?)"
                )
                return
            await callback(interaction, *args, **kwargs)
        except Exception as error:
            await interaction.reply(f"{error.__class__.__name__}: {error}")

    return wrapper


_quit_hooks: list[Function] = []


def on_quit(callback: Function):
    """Decorator for functions to call when the bot quits."""

    _quit_hooks.append(callback)
    return callback


@function
async def quit(interaction: Interaction):
    for quit_hook in _quit_hooks:
        await quit_hook()
    await interaction.reply(":koala:")
    await bot.close()


@bot.tree.command(
    name="quit",
    description="Stop running the bot.",
)
async def quit_discord(interaction: discord.Interaction):
    await quit(SlashCommand(interaction))

import functools

import discord

from domain.analysis import analysis as analysis_
import hideout
from versus.game import Game

channels: list[discord.TextChannel | None] = [None, None]
game = Game()


def opponent(interaction: hideout.Interaction):
    player = channels.index(interaction.channel)
    return channels[1 - player]


def ingame_only(function: hideout.Function):
    """Decorator that only allows functions to be used during a game."""

    @functools.wraps(function)
    async def wrapper(interaction: hideout.Interaction, *args, **kwargs):
        if not game.started:
            await interaction.reply("The game hasn't started yet. (Start a new game?)")
            return
        await function(interaction, *args, **kwargs)

    return wrapper


def player_only(function: hideout.Function):
    """Decorator that only allows functions to be used by players."""

    @functools.wraps(function)
    async def wrapper(interaction: hideout.Interaction, *args, **kwargs):
        if interaction.channel not in channels:
            await interaction.reply("You need to be in one of the two player channels.")
            return
        await function(interaction, *args, **kwargs)

    return wrapper


@hideout.function
async def help(interaction: hideout.Interaction):
    text = "\n".join(command.name for command in hideout.bot.tree.get_commands())
    await interaction.reply("tbd\n" + text)


@hideout.function
async def player(interaction: hideout.Interaction, index: int):
    channels[index] = interaction.channel
    await interaction.reply("You will now use this channel to play the game.")


@hideout.function
async def analysis(interaction: hideout.Interaction, guesses: str):
    await interaction.reply(f"```{analysis_(guesses.split())}```")


@hideout.function
async def reset(interaction: hideout.Interaction):
    game.reset()
    await interaction.reply("You reset the game.")
    for channel in channels:
        if channel == interaction.channel:
            continue
        await channel.send("The game was reset.")


@hideout.function
@player_only
async def start(interaction: hideout.Interaction, word: str, force: bool = False):
    index = channels.index(interaction.channel)
    game.start(index, word, force=force)
    if game.started:
        instance = game.instances[index]
        await interaction.reply(instance.last_guess_formatted())
        await opponent(interaction).send(game.instances[1 - index].last_guess_formatted())
    else:
        await interaction.reply(f"You will choose {word} as your starting word.")


@hideout.function
@ingame_only
@player_only
async def guess(interaction: hideout.Interaction, word: str, force: bool = False):
    index = channels.index(interaction.channel)
    game.make_guess(index, word, force=force)
    instance = game.instances[index]
    await interaction.reply(instance.last_guess_formatted())
    if instance.solved:
        await opponent(interaction).send(
            f"Opponent solved your word in {len(instance.guesses)} guesses."
        )


@hideout.function
@ingame_only
@player_only
async def auto(interaction: hideout.Interaction):
    index = channels.index(interaction.channel)
    game.auto_guess(index)
    instance = game.instances[index]
    await interaction.reply(instance.last_guess_formatted())
    if instance.solved:
        await opponent(interaction).send(
            f"Opponent solved your word in {len(instance.guesses)} guesses."
        )


@hideout.function
@ingame_only
@player_only
async def keyboard(interaction: hideout.Interaction):
    index = channels.index(interaction.channel)
    await interaction.reply(game.keyboard(index).formatted())


@hideout.command(
    name="help",
    description="tbd",
)
async def help_command(interaction: discord.Interaction):
    await help(hideout.SlashCommand(interaction))


@hideout.command(
    name="player1",
    description="Use this channel as Player 1.",
)
async def player_1_command(interaction: discord.Interaction):
    await player(hideout.SlashCommand(interaction), index=0)


@hideout.command(
    name="player2",
    description="Use this channel as Player 2.",
)
async def player_2_command(interaction: discord.Interaction):
    await player(hideout.SlashCommand(interaction), index=1)


@hideout.command(
    name="analysis",
    description="List all possible words given a guess sequence.",
)
async def analysis_command(interaction: discord.Interaction, guesses: str):
    await analysis(hideout.SlashCommand(interaction), guesses)


@hideout.command(
    name="reset",
    description="Reset the game.",
)
async def reset_command(interaction: discord.Interaction):
    await reset(hideout.SlashCommand(interaction))


@hideout.command(
    name="start",
    description="Choose a starting word.",
)
async def start_command(interaction: discord.Interaction, word: str):
    await start(hideout.SlashCommand(interaction), word)


@hideout.command(
    name="forcestart",
    description="Choose a starting word, bypassing normal secret validation.",
)
async def forcestart_command(interaction: discord.Interaction, word: str):
    await start(hideout.SlashCommand(interaction), word, force=True)


@hideout.command(
    name="guess",
    description="Guess a word.",
)
async def guess_command(interaction: discord.Interaction, word: str):
    await guess(hideout.SlashCommand(interaction), word)


@hideout.command(
    name="forceguess",
    description="Guess a word, bypassing normal guess validation.",
)
async def forceguess_command(interaction: discord.Interaction, word: str):
    await guess(hideout.SlashCommand(interaction), word, force=True)


@hideout.command(
    name="auto",
    description="Solve the game if there is only one word left, otherwise make a random guess.",
)
async def auto_command(interaction: discord.Interaction):
    await auto(hideout.SlashCommand(interaction))


@hideout.command(
    name="keyboard",
    description="Show what letters are remaining.",
)
async def keyboard_command(interaction: discord.Interaction):
    await keyboard(hideout.SlashCommand(interaction))


hideout.bot.run()

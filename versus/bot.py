from discord import Client, Intents, Interaction
from discord.app_commands import CommandTree

from config.guild import GUILD
from config.p1_channel import P1_CHANNEL
from config.p2_channel import P2_CHANNEL
from config.token import TOKEN
from domain.analysis import analysis as analysis_
from versus.game import Game
from versus.player import Player


bot = Client(intents=Intents.all())
game = Game()


tree = CommandTree(bot)


@bot.event
async def on_ready():
    await tree.sync(guild=GUILD)
    game.channels.clear()
    game.channels.append(bot.get_channel(P1_CHANNEL))
    game.channels.append(bot.get_channel(P2_CHANNEL))


@tree.command(
    name="help",
    description="tbd",
    guild=GUILD,
)
async def help(interaction: Interaction):
    player = Player.from_interaction(interaction)
    try:
        text = "\n".join(command.name for command in tree.get_commands(guild=GUILD))
        await player.reply("tbd\n" + text)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="reset",
    description="Reset the game.",
    guild=GUILD,
)
async def reset(interaction: Interaction):
    player = Player.from_interaction(interaction)
    try:
        await game.reset(player)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="start",
    description="Choose a starting word.",
    guild=GUILD,
)
async def start(interaction: Interaction, word: str):
    player = Player.from_interaction(interaction)
    try:
        await game.start(player, word)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="forcestart",
    description="Choose a starting word, bypassing normal secret validation.",
    guild=GUILD,
)
async def forcestart(interaction: Interaction, word: str):
    player = Player.from_interaction(interaction)
    try:
        await game.start(player, word, force=True)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="guess",
    description="Guess a word.",
    guild=GUILD,
)
async def guess(interaction: Interaction, word: str):
    player = Player.from_interaction(interaction)
    try:
        await game.make_guess(player, word)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="forceguess",
    description="Guess a word, bypassing normal guess validation.",
    guild=GUILD,
)
async def forceguess(interaction: Interaction, word: str):
    player = Player.from_interaction(interaction)
    try:
        await game.make_guess(player, word, force=True)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="keyboard",
    description="Show what letters are remaining.",
    guild=GUILD,
)
async def keyboard(interaction: Interaction):
    player = Player.from_interaction(interaction)
    try:
        await game.keyboard(player)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="auto",
    description="Solve the game if there is only one word left, otherwise make a random guess.",
    guild=GUILD,
)
async def auto(interaction: Interaction):
    player = Player.from_interaction(interaction)
    try:
        await game.auto_guess(player)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="analysis",
    description="List all possible words given a guess sequence.",
    guild=GUILD,
)
async def analysis(interaction: Interaction, guesses: str):
    player = Player.from_interaction(interaction)
    try:
        await player.reply(f"```{analysis_(guesses.split())}```")
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="quit",
    description="Quit the game.",
    guild=GUILD,
)
async def quit(interaction: Interaction):
    player = Player.from_interaction(interaction)
    await player.reply(":alien:")
    await game.opponent(player).notify("Opponent quit the game.")
    await bot.close()


def start():
    bot.run(TOKEN)

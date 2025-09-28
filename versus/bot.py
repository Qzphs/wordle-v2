from discord import Client, Intents, Interaction
from discord.app_commands import CommandTree

from config.guild import GUILD
from config.p1_channel import P1_CHANNEL
from config.p2_channel import P2_CHANNEL
from config.token import TOKEN
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
    name="guess",
    description="Guess a word.",
    guild=GUILD,
)
async def auto(interaction: Interaction, word: str):
    player = Player.from_interaction(interaction)
    try:
        await game.make_guess(player, word)
    except Exception as e:
        await player.reply(f"{e.__class__.__name__}: {e}")


@tree.command(
    name="auto",
    description="Guess a random word.",
    guild=GUILD,
)
async def auto(interaction: Interaction):
    player = Player.from_interaction(interaction)
    try:
        await game.auto_guess(player)
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

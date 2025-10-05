from discord import TextChannel

from domain.colour import Colour
from domain.instance import IllegalActionError, Instance
from domain.words import validate_secret
from versus.player import Player


COLOUR_EMOJIS = {
    Colour.GRAY: ":black_large_square:",
    Colour.YELLOW: ":yellow_square:",
    Colour.GREEN: ":green_square:",
}


class Game:

    def __init__(self):
        self.channels: list[TextChannel] = []
        self.words: list[str | None] = [None, None]
        self.instances = [Instance(), Instance()]

    @property
    def started(self):
        return None not in self.words

    def opponent(self, player: Player):
        if player.channel == self.channels[0]:
            return Player.from_channel(self.channels[1])
        else:
            return Player.from_channel(self.channels[0])

    async def reset(self, player: Player):
        if player.channel not in self.channels:
            raise IllegalActionError(
                "you need to be in one of the two player channels",
            )
        self.words[0] = None
        self.words[1] = None
        self.instances[0] = Instance()
        self.instances[1] = Instance()
        await player.reply("You reset the game.")
        await self.opponent(player).notify("Opponent reset the game.")

    async def start(self, player: Player, word: str, force: bool = False):
        if self.started:
            raise IllegalActionError(
                "cannot add starting word after game has started",
            )
        if player.channel not in self.channels:
            print(player.channel, self.channels)
            raise IllegalActionError(
                "you need to be in one of the two player channels",
            )
        index = self.channels.index(player.channel)
        word = word.lower()
        validate_secret(word, force=force)
        if self.words[index] is None:
            await self.opponent(player).notify(
                "Opponent has chosen a starting word.",
            )
        self.words[index] = word
        if self.started:
            self.instances[0].init_secret(self.words[1], force=True)
            self.instances[0].make_guess(self.words[0], force=True)
            self.instances[1].init_secret(self.words[0], force=True)
            self.instances[1].make_guess(self.words[1], force=True)
            index = self.channels.index(player.channel)
            await player.reply(self._guess_result(self.instances[index]))
            await self.opponent(player).notify(
                self._guess_result(self.instances[1 - index])
            )
        else:
            await player.reply(
                f"You will use **{word}** as your starting word.",
            )

    async def make_guess(self, player: Player, word: str, force: bool = False):
        if not self.started:
            raise IllegalActionError("cannot guess before game has started")
        if player.channel not in self.channels:
            raise IllegalActionError(
                "you need to be in one of the two player channels",
            )
        index = self.channels.index(player.channel)
        instance = self.instances[index]
        instance.make_guess(word, force=force)
        await player.reply(self._guess_result(instance))
        if instance.solved:
            await self.opponent(player).notify(
                f"Opponent solved your word in {len(instance.guesses)} guesses.",
            )

    async def auto_guess(self, player: Player):
        if not self.started:
            raise IllegalActionError("cannot guess before game has started")
        if player.channel not in self.channels:
            raise IllegalActionError(
                "you need to be in one of the two player channels",
            )
        index = self.channels.index(player.channel)
        instance = self.instances[index]
        instance.auto_guess()
        await player.reply(self._guess_result(instance))
        if instance.solved:
            await self.opponent(player).notify(
                f"Opponent solved your word in {len(instance.guesses)} guesses.",
            )

    def _guess_result(self, instance: Instance):
        word = " ".join(
            f":regional_indicator_{letter}:" for letter in instance.guesses[-1]
        )
        hint = " ".join(COLOUR_EMOJIS[colour] for colour in instance.hints[-1].colours)
        return f"guess {len(instance.guesses)}/6:\n{word}\n{hint}"

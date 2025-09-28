from domain.colour import Colour
from domain.word import Word


class InvalidHintError(Exception):
    pass


class Hint:

    def __init__(self, *colours: Colour):
        self.colours = list(colours)
        if len(self.colours) != 5:
            raise InvalidHintError(f"invalid hint {self.colours}")

    @classmethod
    def all_gray(cls):
        return Hint(
            Colour.GRAY,
            Colour.GRAY,
            Colour.GRAY,
            Colour.GRAY,
            Colour.GRAY,
        )

    @classmethod
    def from_words(cls, guess: str | Word, secret: str | Word):
        if isinstance(guess, str):
            guess = Word(guess)
        if isinstance(secret, str):
            secret = Word(secret)
        colours = [Colour.GRAY for _ in range(5)]
        remaining = list(secret.letters)
        for i in range(5):
            if guess.letters[i] != secret.letters[i]:
                continue
            colours[i] = Colour.GREEN
            remaining.remove(guess.letters[i])
        for i in range(5):
            if colours[i] == Colour.GREEN:
                continue
            if guess.letters[i] not in remaining:
                continue
            colours[i] = Colour.YELLOW
            remaining.remove(guess.letters[i])
        return Hint(*colours)

    def __eq__(self, other):
        if not isinstance(other, Hint):
            return NotImplemented
        return self.colours == other.colours

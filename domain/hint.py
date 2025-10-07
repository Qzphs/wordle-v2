from domain.colour import Colour
from domain.words import validate_word


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
    def from_words(cls, guess: str, secret: str):
        guess = guess.lower()
        secret = secret.lower()
        validate_word(guess)
        validate_word(secret)

        colours = [Colour.GRAY for _ in range(5)]
        remaining = list(secret)
        for i in range(5):
            if guess[i] != secret[i]:
                continue
            colours[i] = Colour.GREEN
            remaining.remove(guess[i])
        for i in range(5):
            if colours[i] == Colour.GREEN:
                continue
            if guess[i] not in remaining:
                continue
            colours[i] = Colour.YELLOW
            remaining.remove(guess[i])
        return Hint(*colours)

    def __eq__(self, other):
        if not isinstance(other, Hint):
            return NotImplemented
        return self.colours == other.colours

    def formatted(self):
        return " ".join(colour.emoji for colour in self.colours)

from domain.colour import Colour
from domain.hint import Hint


class Keyboard:

    def __init__(self):
        self.letters = {letter: 0 for letter in "abcdefghijklmnopqrstuvwxyz"}

    def update(self, guess: str, hint: Hint):
        for letter, colour in zip(guess, hint.colours):
            self.letters[letter] = max(self.letters[letter], self._priority(colour))

    def _priority(self, colour: Colour):
        if colour == Colour.GRAY:
            return 1
        elif colour == Colour.YELLOW:
            return 2
        elif colour == Colour.GREEN:
            return 3

    def formatted(self):
        rows = [
            "remaining letters:",
            self._letter_row("qwertyuiop"),
            self._colour_row("qwertyuiop"),
            self._letter_row("asdfghjkl"),
            self._colour_row("asdfghjkl"),
            self._letter_row("zxcvbnm"),
            self._colour_row("zxcvbnm"),
        ]
        return "\n".join(rows)

    def _letter_row(self, letters: str):
        return " ".join(f":regional_indicator_{letter}:" for letter in letters)

    def _colour_row(self, letters: str):
        return " ".join(self._colour(letter) for letter in letters)

    def _colour(self, letter: str):
        priority = self.letters[letter]
        if priority == 0:
            return ":white_large_square:"
        elif priority == 1:
            return ":black_large_square:"
        elif priority == 2:
            return ":yellow_square:"
        elif priority == 3:
            return ":green_square:"

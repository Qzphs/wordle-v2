import random

from domain.hint import Hint
from domain.word import SECRETS, Word


class IllegalActionError(Exception):
    pass


class Instance:

    def __init__(self):
        self.secret: Word | None = None
        self.candidates = [Word(secret) for secret in SECRETS]
        self.guesses: list[Word] = []
        self.hints: list[Hint] = []

    @property
    def solved(self):
        if not self.guesses:
            return False
        return self.guesses[-1] == self.secret

    def init_secret(self, secret: str | Word):
        if self.secret is not None:
            raise IllegalActionError("cannot re-initialise secret")
        if isinstance(secret, str):
            secret = Word(secret)
        secret.validate_secret()
        self.secret = secret

    def make_guess(self, guess: str | Word):
        if self.secret is None:
            raise IllegalActionError(
                "cannot make guess before secret initialised",
            )
        if isinstance(guess, str):
            guess = Word(guess)
        guess.validate_guess()
        self.guesses.append(guess)
        hint = Hint.from_words(guess, self.secret)
        remaining = [
            candidate
            for candidate in self.candidates
            if Hint.from_words(guess, candidate) == hint
        ]
        self.candidates.clear()
        self.candidates.extend(remaining)
        self.hints.append(hint)

    def auto_guess(self):
        if self.secret is None:
            raise IllegalActionError(
                "cannot make guess before secret initialised",
            )
        if len(self.candidates) == 1:
            self.make_guess(self.secret)
        else:
            guesses = self.candidates.copy()
            guesses.remove(self.secret)
            self.make_guess(random.choice(guesses))

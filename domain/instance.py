import random

from domain.hint import Hint
from domain.words import SECRETS, validate_guess, validate_secret, validate_word


class IllegalActionError(Exception):
    pass


class Instance:

    def __init__(self):
        self.secret: str | None = None
        self.candidates = list(SECRETS)
        self.guesses: list[str] = []
        self.hints: list[Hint] = []

    @property
    def solved(self):
        if not self.guesses:
            return False
        return self.guesses[-1] == self.secret

    def init_secret(self, secret: str, force: bool = False):
        if self.secret is not None:
            raise IllegalActionError("cannot re-initialise secret")
        secret = secret.lower()
        validate_secret(secret, force=force)
        self.secret = secret
        if secret not in self.candidates:
            self.candidates.append(secret)

    def make_guess(self, guess: str, force: bool = False):
        if self.secret is None:
            raise IllegalActionError(
                "cannot make guess before secret initialised",
            )
        guess = guess.lower()
        validate_guess(guess, force=force)
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
            self.make_guess(self.secret, force=True)
        else:
            guesses = self.candidates.copy()
            guesses.remove(self.secret)
            self.make_guess(random.choice(guesses), force=True)

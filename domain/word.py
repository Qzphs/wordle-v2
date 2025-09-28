with open("guesses.txt") as file:
    GUESSES = sorted(file.read().split())


with open("secrets.txt") as file:
    SECRETS = sorted(file.read().split())


class InvalidWordError(Exception):
    pass


class Word:

    def __init__(self, letters: str):
        if len(letters) != 5:
            raise InvalidWordError(f"'{self.letters}' does not have 5 letters")
        if not letters.isalpha():
            raise InvalidWordError(f"'{self.letters}' contains invalid letters")
        self.letters = letters.lower()

    def validate_guess(self):
        if self.letters in GUESSES:
            return
        raise InvalidWordError(f"'{self.letters}' not a guess")

    def validate_secret(self):
        if self.letters in SECRETS:
            return
        raise InvalidWordError(f"'{self.letters}' not a secret")

    def __eq__(self, other):
        if not isinstance(other, Word):
            return NotImplemented
        return self.letters == other.letters

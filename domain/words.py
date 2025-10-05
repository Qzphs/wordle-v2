with open("guesses.txt") as file:
    GUESSES = sorted(file.read().split())


with open("secrets.txt") as file:
    SECRETS = sorted(file.read().split())


class InvalidWordError(Exception):
    pass


def validate_word(word: str):
    if not word.isalpha():
        raise InvalidWordError(f"{word} contains non-alphabetical characters")
    if len(word) != 5:
        raise InvalidWordError(f"{word} is not 5 letters long")


def validate_guess(word: str, force: bool = False):
    validate_word(word)
    if force:
        return
    if word not in GUESSES:
        raise InvalidWordError(f"{word} not in list of valid guesses")


def validate_secret(word: str, force: bool = False):
    validate_word(word)
    if force:
        return
    if word not in SECRETS:
        raise InvalidWordError(f"{word} not in list of valid secrets")

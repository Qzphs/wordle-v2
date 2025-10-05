from domain.instance import Instance


def analysis(guesses: list[str]):
    for i, guess in enumerate(guesses):
        guesses[i] = guess.lower()
    secret = guesses.pop()
    instance = Instance()
    instance.init_secret(secret, force=True)
    for guess in guesses:
        instance.make_guess(guess, force=True)
    return instance.candidates

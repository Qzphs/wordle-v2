from domain.instance import IllegalActionError, Instance
from domain.words import validate_secret


class Game:

    def __init__(self):
        self.words: list[str | None] = [None, None]
        self.instances = [Instance(), Instance()]

    @property
    def started(self):
        return None not in self.words

    def reset(self):
        self.words[0] = None
        self.words[1] = None
        self.instances[0] = Instance()
        self.instances[1] = Instance()

    def start(self, player: int, word: str, force: bool = False):
        if self.started:
            raise IllegalActionError("cannot change starting word after game has started")
        word = word.lower()
        validate_secret(word, force=force)
        self.words[player] = word
        if self.started:
            self.instances[0].init_secret(self.words[1], force=True)
            self.instances[0].make_guess(self.words[0], force=True)
            self.instances[1].init_secret(self.words[0], force=True)
            self.instances[1].make_guess(self.words[1], force=True)

    def make_guess(self, player: int, word: str, force: bool = False):
        if not self.started:
            raise IllegalActionError("cannot guess before game has started")
        instance = self.instances[player]
        instance.make_guess(word, force=force)

    def keyboard(self, player: int):
        instance = self.instances[player]
        return instance.keyboard

    def auto_guess(self, player: int):
        instance = self.instances[player]
        instance.auto_guess()

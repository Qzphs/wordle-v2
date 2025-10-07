from enum import Enum


class Colour(Enum):

    GRAY = ":black_large_square:"
    YELLOW = ":yellow_square:"
    GREEN = ":green_square:"

    @property
    def emoji(self) -> str:
        return self.value

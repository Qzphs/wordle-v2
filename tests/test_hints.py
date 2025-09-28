import pytest

from domain.colour import Colour
from domain.hint import Hint


def test_hint_arose_alien():
    assert Hint.from_words("arose", "alien") == Hint(
        Colour.GREEN, Colour.GRAY, Colour.GRAY, Colour.GRAY, Colour.YELLOW
    )

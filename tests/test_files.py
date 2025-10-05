import pytest

from domain.words import (
    GUESSES,
    SECRETS,
    InvalidWordError,
    validate_guess,
    validate_secret,
)


def test_guesses_valid():
    try:
        for guess in GUESSES:
            validate_guess(guess)
    except InvalidWordError:
        pytest.fail()


def test_secrets_valid():
    try:
        for secret in SECRETS:
            validate_secret(secret)
    except InvalidWordError:
        pytest.fail()


def test_guesses_superset_secrets():
    assert set(GUESSES).issuperset(SECRETS)

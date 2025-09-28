import pytest

from domain.word import GUESSES, SECRETS


def test_guesses_valid():
    assert all(len(guess) == 5 for guess in GUESSES)


def test_secrets_valid():
    assert all(len(secret) == 5 for secret in SECRETS)


def test_guesses_superset_secrets():
    assert set(GUESSES).issuperset(SECRETS)

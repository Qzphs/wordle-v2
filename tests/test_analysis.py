import pytest

from domain.analysis import analysis


def test_analysis_swamp():
    candidates = analysis(["mimic", "swath", "swamp"])
    assert len(candidates) == 2
    assert "swamp" in candidates
    assert "swarm" in candidates

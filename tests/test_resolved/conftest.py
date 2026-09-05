"""Shared fixtures for the ``test_resolved`` suite.

Only the real-data fixtures this feature's tests need are mirrored here
from ``tests/test_config/conftest.py`` - this package doesn't (yet) have
the full discovery/sweep machinery test_config/test_state have; it's
scoped strictly to what specs/003-single-unit-movement adds
(``ResolvedSystem`` + ``GameStateResolver.resolved_system``), per
plan.md's Project Structure note that closing the broader pre-existing
``tests/test_resolved`` gap is out of this feature's scope.
"""
from pathlib import Path

import pytest

from app.config.ruleset_config import RulesetConfig

@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path("data")

@pytest.fixture(scope="session")
def ruleset_config(data_dir: Path) -> RulesetConfig:
    """The full ruleset, loaded once from the real data/ tree."""
    return RulesetConfig.load(data_dir)

"""Shared fixtures for the ``test_state`` suite.

Mirrors ``tests/test_config/conftest.py``'s fixture philosophy - fixtures
only ever *provide resources*, every ``assert`` lives in a ``test_``
function. State has no equivalent to Config's session-scoped real-data
fixture: State is live, mutable, per-game data with no static on-disk source
of truth to load (see ARCHITECTURE.md section 1's "who owns what" table).
Discovery fixtures mirror Config's exactly, retargeted at ``app.state``.

Deliberately NOT mirrored from ``test_config``: the mutable-container-
violations sweep. Config forbids raw ``dict``/``list``/``set`` fields; State
*requires* them for genuinely mutable per-game data (e.g.
``GameState.deployed_units: dict[str, UnitState]``,
``PlayerState.secret_objective_card_ids_in_hand: set[str]``,
``CardDeckState.deck: list[TCard]``) - porting that Config-only rule here
would be a design mistake, not a safety net.
"""
from __future__ import annotations

import dataclasses
import importlib
import inspect
import pkgutil

import pytest

import app.state as app_state_pkg
from app.config.shared.enum import SerializableEnum

# ---------------------------------------------------------------------------
# Discovery: every dataclass / enum actually defined under app.state
# ---------------------------------------------------------------------------

def _iter_state_modules():
    yield app_state_pkg
    for module_info in pkgutil.walk_packages(app_state_pkg.__path__, prefix="app.state."):
        yield importlib.import_module(module_info.name)

def _discover_state_dataclasses() -> list[type]:
    found: dict[str, type] = {}
    for module in _iter_state_modules():
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if dataclasses.is_dataclass(obj) and obj.__module__.startswith("app.state"):
                found[f"{obj.__module__}.{obj.__qualname__}"] = obj
    return [found[key] for key in sorted(found)]

def _discover_state_enums() -> list[type]:
    found: dict[str, type] = {}
    for module in _iter_state_modules():
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, SerializableEnum)
                and obj is not SerializableEnum
                and obj.__module__.startswith("app.state")
            ):
                found[f"{obj.__module__}.{obj.__qualname__}"] = obj
    return [found[key] for key in sorted(found)]

@pytest.fixture(scope="session")
def all_state_dataclasses() -> list[type]:
    return _discover_state_dataclasses()

@pytest.fixture(scope="session")
def all_state_enums() -> list[type]:
    return _discover_state_enums()

def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrize sweep tests one test-id per discovered class."""
    if "state_dataclass" in metafunc.fixturenames:
        classes = _discover_state_dataclasses()
        metafunc.parametrize("state_dataclass", classes, ids=[c.__qualname__ for c in classes])
    if "state_enum" in metafunc.fixturenames:
        enums = _discover_state_enums()
        metafunc.parametrize("state_enum", enums, ids=[e.__qualname__ for e in enums])

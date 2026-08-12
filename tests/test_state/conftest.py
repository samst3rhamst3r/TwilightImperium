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

Partially mirrored, scoped down: ``declared_immutable_field_violations`` is
the State analog of Config's ``runtime_mutability_violations``, but only
checks the subset of fields a State class itself chose to declare
``tuple[...]``/``MappingProxyType[...]`` (optionally ``Optional[...]``) -
not a blanket "everything must be immutable" sweep. Per-class tests call it
on a constructed/loaded instance, not as a class-wide parametrized sweep.
"""
from __future__ import annotations

import dataclasses
import importlib
import inspect
import pkgutil
from types import MappingProxyType, UnionType
from typing import Union, get_args, get_origin, get_type_hints

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

# ---------------------------------------------------------------------------
# Reusable computation - fields State itself chose to declare immutable
# (tuple[...] / MappingProxyType[...], including Optional[...] of either)
# must actually hold that runtime type, not a plain list/dict. Unlike Config's
# mutable_container_violations, this does NOT forbid bare dict/list/set fields
# outright - State legitimately has plenty of those. It only checks the
# subset of fields a class opted into immutability for.
# ---------------------------------------------------------------------------

_IMMUTABLE_ORIGINS = (tuple, MappingProxyType)

def _immutable_declared_origin(tp):
    """Return the tuple/MappingProxyType origin a type hint declares, unwrapping
    one level of Optional/Union, or None if the hint isn't one of those."""
    origin = get_origin(tp)
    if origin in _IMMUTABLE_ORIGINS:
        return origin
    if origin in (Union, UnionType):
        for arg in get_args(tp):
            if arg is type(None):
                continue
            arg_origin = get_origin(arg)
            if arg_origin in _IMMUTABLE_ORIGINS:
                return arg_origin
    return None

@pytest.fixture
def declared_immutable_field_violations():
    """Factory: instance -> list[str] of fields declared tuple[...]/
    MappingProxyType[...] (optionally wrapped in Optional[...]) whose actual
    runtime value isn't that type (empty if clean). Catches the exact class of
    bug found in GameState.init_from_save, where MappingProxyType-declared
    fields were assigned plain dict literals on load."""
    def _violations(instance) -> list[str]:
        cls = type(instance)
        hints = get_type_hints(cls)
        violations: list[str] = []
        for f in dataclasses.fields(cls):
            declared_origin = _immutable_declared_origin(hints[f.name])
            if declared_origin is None:
                continue
            value = getattr(instance, f.name)
            if value is None:
                continue  # legitimately-unset Optional[tuple/MappingProxyType] field
            if not isinstance(value, declared_origin):
                violations.append(
                    f"{cls.__name__}.{f.name} is declared to hold "
                    f"{declared_origin.__name__} but the runtime value is a "
                    f"{type(value).__name__!r}"
                )
        return violations
    return _violations

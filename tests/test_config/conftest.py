"""Shared fixtures for the ``test_config`` suite.

Fixtures here only ever *provide resources* (paths, loaded data, discovered
classes, pure-computation helper callables) - they never assert anything.
Every ``assert`` lives in a ``test_`` function, in this file's sibling
modules, which mirror ``src/app/config``'s package layout one-for-one.

- ``data_dir`` / ``ruleset_config`` - the real YAML content under ``data/``,
  loaded exactly once per session (mirrors ``RulesetConfig``'s own
  load-once/shared-across-games design; see ARCHITECTURE.md section 2).
- ``all_config_dataclasses`` / ``all_config_enums`` - every dataclass/enum
  actually defined under ``app.config``, discovered by walking the package.
  ``pytest_generate_tests`` below uses these to parametrize the structural
  sweeps in ``test_config_invariants.py`` one test-id per class, so a new
  Config class added later is covered automatically.
- ``mutable_container_violations`` - a factory that inspects a dataclass's
  field type hints and *returns* a list of violation strings (empty if
  clean). It performs no assertions itself; callers assert the list is empty.
"""
from __future__ import annotations

import dataclasses
import importlib
import inspect
import pkgutil
from pathlib import Path
from types import MappingProxyType, UnionType
from typing import Union, get_args, get_origin, get_type_hints

import pytest

import app.config as app_config_pkg
from app.config.ruleset_config import RulesetConfig
from app.config.shared.enum import ConfigEnum, SerializableEnum

# ---------------------------------------------------------------------------
# Data fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path("data")

@pytest.fixture(scope="session")
def data_objs_dir(data_dir: Path) -> Path:
    return data_dir / "objs"

@pytest.fixture(scope="session")
def text_objs_dir(data_dir: Path) -> Path:
    return data_dir / "text_objs"

@pytest.fixture(scope="session")
def ruleset_config(data_dir: Path) -> RulesetConfig:
    """The full ruleset, loaded once from the real data/ tree."""
    return RulesetConfig.load(data_dir)

# ---------------------------------------------------------------------------
# Discovery: every dataclass / enum actually defined under app.config
# ---------------------------------------------------------------------------

def _iter_config_modules():
    yield app_config_pkg
    for module_info in pkgutil.walk_packages(app_config_pkg.__path__, prefix="app.config."):
        yield importlib.import_module(module_info.name)

def _discover_config_dataclasses() -> list[type]:
    found: dict[str, type] = {}
    for module in _iter_config_modules():
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if dataclasses.is_dataclass(obj) and obj.__module__.startswith("app.config"):
                found[f"{obj.__module__}.{obj.__qualname__}"] = obj
    return [found[key] for key in sorted(found)]

def _discover_config_enums() -> list[type]:
    found: dict[str, type] = {}
    for module in _iter_config_modules():
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, SerializableEnum)
                and obj not in (SerializableEnum, ConfigEnum)
                and obj.__module__.startswith("app.config")
            ):
                found[f"{obj.__module__}.{obj.__qualname__}"] = obj
    return [found[key] for key in sorted(found)]

@pytest.fixture(scope="session")
def all_config_dataclasses() -> list[type]:
    return _discover_config_dataclasses()

@pytest.fixture(scope="session")
def all_config_enums() -> list[type]:
    return _discover_config_enums()

def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrize sweep tests one test-id per discovered class."""
    if "config_dataclass" in metafunc.fixturenames:
        classes = _discover_config_dataclasses()
        metafunc.parametrize("config_dataclass", classes, ids=[c.__qualname__ for c in classes])
    if "config_enum" in metafunc.fixturenames:
        enums = _discover_config_enums()
        metafunc.parametrize("config_enum", enums, ids=[e.__qualname__ for e in enums])

# ---------------------------------------------------------------------------
# Reusable computation - mutable/generic container detection
# ---------------------------------------------------------------------------

_DISALLOWED_BARE_CONTAINERS = (dict, list, set)

def _describe(tp) -> str:
    return getattr(tp, "__name__", str(tp))

def _container_violations_for_type(tp, *, field_name: str, owner: type) -> list[str]:
    origin = get_origin(tp)

    if origin is None:
        if inspect.isclass(tp) and issubclass(tp, _DISALLOWED_BARE_CONTAINERS):
            return [
                f"{owner.__name__}.{field_name} is typed as bare '{_describe(tp)}' - "
                "mutable/non-tuple containers are disallowed; use tuple[...] for "
                "sequences or MappingProxyType[...] for mappings."
            ]
        return []

    if origin in (Union, UnionType):
        violations = []
        for arg in get_args(tp):
            violations.extend(_container_violations_for_type(arg, field_name=field_name, owner=owner))
        return violations

    if origin is tuple:
        violations = []
        for arg in get_args(tp):
            if arg is not Ellipsis:
                violations.extend(_container_violations_for_type(arg, field_name=field_name, owner=owner))
        return violations

    if origin is MappingProxyType:
        violations = []
        for arg in get_args(tp):
            violations.extend(_container_violations_for_type(arg, field_name=field_name, owner=owner))
        return violations

    return [
        f"{owner.__name__}.{field_name} is typed with disallowed generic container "
        f"'{_describe(origin)}[...]' - only tuple[...] (sequences) and "
        "MappingProxyType[...] (mappings) are allowed on Config dataclasses."
    ]

@pytest.fixture
def mutable_container_violations():
    """Factory: cls -> list[str] of field-*typing* violations (empty if clean).

    This only inspects declared type hints - see runtime_mutability_violations
    below for the complementary check on actual instance data.
    """
    def _violations(cls: type) -> list[str]:
        hints = get_type_hints(cls)
        violations: list[str] = []
        for f in dataclasses.fields(cls):
            violations.extend(_container_violations_for_type(hints[f.name], field_name=f.name, owner=cls))
        return violations
    return _violations

# ---------------------------------------------------------------------------
# Reusable computation - recursive *runtime* immutability of a real object graph
# ---------------------------------------------------------------------------

def _runtime_violations(obj, *, path: str, seen: set[int]) -> list[str]:
    if type(obj) in (list, dict, set):
        return [
            f"{path} is a runtime {type(obj).__name__!r} - every collection must be "
            "frozen (tuple / MappingProxyType) all the way down, not just at the top level"
        ]

    obj_id = id(obj)
    if obj_id in seen:
        return []  # already walked (or currently walking) this object - avoid cycles
    seen = seen | {obj_id}

    if isinstance(obj, MappingProxyType):
        violations: list[str] = []
        for key, value in obj.items():
            violations.extend(_runtime_violations(key, path=f"{path}[key={key!r}]", seen=seen))
            violations.extend(_runtime_violations(value, path=f"{path}[{key!r}]", seen=seen))
        return violations

    if isinstance(obj, tuple):
        violations = []
        for i, item in enumerate(obj):
            violations.extend(_runtime_violations(item, path=f"{path}[{i}]", seen=seen))
        return violations

    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        violations = []
        for f in dataclasses.fields(obj):
            violations.extend(
                _runtime_violations(getattr(obj, f.name), path=f"{path}.{f.name}", seen=seen)
            )
        return violations

    return []  # primitive / enum / str / Path / etc. - a leaf, nothing to recurse into

@pytest.fixture
def runtime_mutability_violations():
    """Factory: obj -> list[str] of mutable-container sightings anywhere in
    its object graph (empty if the whole graph is frozen). Walks dataclass
    fields, tuple elements, and MappingProxyType keys/values recursively."""
    def _violations(obj) -> list[str]:
        return _runtime_violations(obj, path=type(obj).__name__, seen=set())
    return _violations
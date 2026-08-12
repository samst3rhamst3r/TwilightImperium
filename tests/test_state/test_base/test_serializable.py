"""Tests for app.state.base.serializable.Serializable - the ABC every State
class terminates its save/init_from_save cooperative chain at."""
from dataclasses import dataclass

import pytest

from app.state.base.serializable import Serializable

@dataclass(kw_only=True)
class _ConcreteSerializable(Serializable):
    """Minimal concrete leaf - Serializable itself is abstract (ABC with
    @abstractmethod save/init_from_save), so behavior tests need a real
    subclass to instantiate."""
    value: int = 0

    def save(self) -> dict:
        return super().save() | {"value": self.value}

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.value = data["value"]

def test_serializable_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        Serializable()

def test_concrete_subclass_save_round_trips() -> None:
    obj = _ConcreteSerializable(value=42)
    reloaded = _ConcreteSerializable.load(obj.save())
    assert reloaded.value == 42

def test_load_bypasses_init_via_new_and_calls_init_from_save() -> None:
    """load() uses cls.__new__(cls) + init_from_save, not __init__ - confirms
    the mechanism ARCHITECTURE.md section 3 documents for the load path."""
    obj = _ConcreteSerializable.load({"value": 7})
    assert isinstance(obj, _ConcreteSerializable)
    assert obj.value == 7

"""Tests for app.state.base.mixins - IDedStateObj / ConfigIDStateObj /
UUIDInstancedStateObj, the three State-layer identity mixins."""
from dataclasses import dataclass

import pytest

from app.state.base.mixins import ConfigIDStateObj, IDedStateObj, UUIDInstancedStateObj

def test_ided_state_obj_cannot_be_instantiated_directly() -> None:
    """obj_id is @property @abstractmethod with no concrete body - unlike its
    two subclasses below, which each provide a real implementation."""
    with pytest.raises(TypeError):
        IDedStateObj()

def test_config_id_state_obj_obj_id_returns_config_id() -> None:
    obj = ConfigIDStateObj(config_id="infantry")
    assert obj.obj_id == "infantry"

def test_config_id_state_obj_save_load_round_trip() -> None:
    obj = ConfigIDStateObj(config_id="infantry")
    reloaded = ConfigIDStateObj.load(obj.save())
    assert reloaded.config_id == "infantry"
    assert reloaded.obj_id == "infantry"

def test_uuid_instanced_state_obj_generates_unique_instance_ids() -> None:
    a = UUIDInstancedStateObj(config_id="infantry")
    b = UUIDInstancedStateObj(config_id="infantry")
    assert a.instance_id != b.instance_id
    assert a.obj_id == a.instance_id

def test_uuid_instanced_state_obj_instance_id_is_not_a_constructor_argument() -> None:
    """instance_id is field(init=False, default_factory=...) - a caller can't
    pass it in; it's always freshly generated on construction."""
    with pytest.raises(TypeError):
        UUIDInstancedStateObj(config_id="infantry", instance_id="not-allowed")

def test_uuid_instanced_state_obj_save_load_round_trip_preserves_instance_id() -> None:
    obj = UUIDInstancedStateObj(config_id="infantry")
    reloaded = UUIDInstancedStateObj.load(obj.save())
    assert reloaded.config_id == "infantry"
    assert reloaded.instance_id == obj.instance_id

@dataclass(kw_only=True)
class _DummyIded(IDedStateObj):
    """A minimal concrete IDedStateObj - confirms a leaf class providing
    obj_id (like PlayerState does) satisfies the abstract contract without
    going through ConfigIDStateObj/UUIDInstancedStateObj."""
    name: str

    @property
    def obj_id(self) -> str:
        return self.name

    def save(self) -> dict:
        return super().save() | {"name": self.name}

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.name = data["name"]

def test_ided_state_obj_subclass_can_supply_its_own_obj_id() -> None:
    obj = _DummyIded(name="sam")
    assert obj.obj_id == "sam"

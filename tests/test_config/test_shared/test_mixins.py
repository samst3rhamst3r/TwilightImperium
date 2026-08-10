"""Mirrors src/app/config/shared/mixins.py."""
import pytest

from app.config.shared.mixins import (
    CanBeExhaustible,
    CanHaveFactionExclusivity,
    RequiresFlavorText,
    RequiresFlavorTextOptions,
    RequiresFunctionalText,
)

_ALL_MIXINS = (
    RequiresFunctionalText,
    RequiresFlavorText,
    RequiresFlavorTextOptions,
    CanHaveFactionExclusivity,
    CanBeExhaustible,
)

@pytest.mark.parametrize("mixin", _ALL_MIXINS, ids=[m.__name__ for m in _ALL_MIXINS])
def test_mixins_are_deliberately_not_slotted(mixin: type) -> None:
    """CPython's multiple inheritance only tolerates one base in the MRO
    contributing real (non-empty) __slots__. Concrete Config classes combine
    two or more of these mixins with NamedConfigObj/IDConfigObj (which IS
    slotted), so giving every mixin its own slots would raise
    "TypeError: multiple bases have instance lay-out conflict" the moment two
    of them are combined - this is exactly the bug that blocked importing
    app.config entirely until it was fixed."""
    assert not mixin.__dataclass_params__.slots

def test_can_have_faction_exclusivity_defaults_to_not_exclusive() -> None:
    obj = CanHaveFactionExclusivity()
    assert obj.faction_exclusive_id is None
    assert obj.is_faction_exclusive is False

def test_can_have_faction_exclusivity_reports_exclusivity_correctly() -> None:
    obj = CanHaveFactionExclusivity(faction_exclusive_id="jol_nar")
    assert obj.is_faction_exclusive is True
    assert obj.is_exclusive_to("jol_nar") is True
    assert obj.is_exclusive_to("sol") is False

def test_can_be_exhaustible_defaults_to_false() -> None:
    assert CanBeExhaustible().exhaustible is False

def test_requires_functional_text_field_is_mandatory() -> None:
    with pytest.raises(TypeError):
        RequiresFunctionalText()

def test_requires_flavor_text_field_is_mandatory() -> None:
    with pytest.raises(TypeError):
        RequiresFlavorText()

def test_requires_flavor_text_options_field_is_mandatory() -> None:
    with pytest.raises(TypeError):
        RequiresFlavorTextOptions()

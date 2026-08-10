"""Mirrors src/app/config/shared/enum.py."""
from enum import auto

import pytest

from app.config.shared.enum import ConfigEnum, MissingEnumMemberError, NotLowerCasedValueError, SerializableEnum

class _SampleConfigEnum(ConfigEnum):
    ALPHA = auto()
    BETA = auto()

def test_configenum_is_a_serializable_enum() -> None:
    assert issubclass(ConfigEnum, SerializableEnum)

def test_serializable_enum_repr_is_qualified_by_class_name() -> None:
    assert repr(_SampleConfigEnum.ALPHA) == "_SampleConfigEnum.ALPHA"

def test_configenum_member_equals_its_lowercased_string_value() -> None:
    assert _SampleConfigEnum.ALPHA == "alpha"

def test_configenum_accepts_the_lowercased_value() -> None:
    assert _SampleConfigEnum("alpha") is _SampleConfigEnum.ALPHA

def test_configenum_rejects_wrong_case_with_a_specific_error() -> None:
    """This is the whole point of ConfigEnum over plain SerializableEnum:
    YAML data that accidentally writes "Alpha" instead of "alpha" must fail
    loudly, not silently coerce."""
    with pytest.raises(NotLowerCasedValueError):
        _SampleConfigEnum("ALPHA")

def test_configenum_rejects_unknown_values_with_a_different_error() -> None:
    with pytest.raises(MissingEnumMemberError):
        _SampleConfigEnum("gamma")

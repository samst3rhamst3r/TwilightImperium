"""Mirrors src/app/config/objs/index.py."""
from types import MappingProxyType

import pytest

from app.config.objs.id import IDConfigObj
from app.config.objs.index import DuplicateConfigIDError, index_by_id

def test_index_by_id_keys_each_config_by_its_id() -> None:
    a, b = IDConfigObj(id="a"), IDConfigObj(id="b")
    index = index_by_id([a, b])
    assert isinstance(index, MappingProxyType)
    assert dict(index) == {"a": a, "b": b}

def test_index_by_id_accepts_a_generator() -> None:
    index = index_by_id(IDConfigObj(id=i) for i in ("a", "b"))
    assert set(index) == {"a", "b"}

def test_index_by_id_is_read_only() -> None:
    index = index_by_id([IDConfigObj(id="a")])
    with pytest.raises(TypeError):
        index["b"] = IDConfigObj(id="b")

def test_index_by_id_rejects_duplicate_ids() -> None:
    """Every per-type loader indexes through this, so a copy-pasted YAML id
    fails loudly at load time instead of silently dropping an entry."""
    with pytest.raises(DuplicateConfigIDError):
        index_by_id([IDConfigObj(id="a"), IDConfigObj(id="a")])

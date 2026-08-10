"""Mirrors src/app/config/shared/named.py."""
from app.config.shared.id import IDConfigObj
from app.config.shared.named import NamedConfigObj

def test_named_config_obj_inherits_id_config_obj() -> None:
    assert issubclass(NamedConfigObj, IDConfigObj)

def test_str_resolves_to_name_not_id() -> None:
    """NamedConfigObj and IDConfigObj both define __str__ - a textbook
    same-named-method-on-multiple-bases scenario. MRO puts NamedConfigObj
    (the more-derived class) ahead of IDConfigObj, so its version wins
    deterministically rather than ambiguously."""
    obj = NamedConfigObj(id="some_id", name="Some Name")
    assert str(obj) == "Some Name"
    assert str(obj) != obj.id

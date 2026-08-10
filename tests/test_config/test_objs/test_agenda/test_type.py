"""Mirrors src/app/config/objs/agenda/type.py."""
from app.config.objs.agenda import AgendaType
from app.config.shared.enum import ConfigEnum

def test_agenda_type_is_a_configenum() -> None:
    assert issubclass(AgendaType, ConfigEnum)

def test_agenda_type_has_the_expected_members() -> None:
    assert {member.value for member in AgendaType} == {"directive", "law"}

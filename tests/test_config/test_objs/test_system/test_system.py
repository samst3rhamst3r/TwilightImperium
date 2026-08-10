"""Mirrors src/app/config/objs/system/system.py."""
from app.config.objs.system import SystemConfig
from app.config.shared import IDConfigObj

def test_system_config_inherits_id_config_obj() -> None:
    assert issubclass(SystemConfig, IDConfigObj)

def test_back_color_is_required_but_nullable() -> None:
    """back_color has no default - callers must explicitly pass None (e.g.
    for Mecatol Rex) rather than it silently defaulting, per the comment in
    system.py."""
    import dataclasses

    field = next(f for f in dataclasses.fields(SystemConfig) if f.name == "back_color")
    assert field.default is dataclasses.MISSING

def test_real_mecatol_rex_system_has_no_back_color(ruleset_config) -> None:
    mecatol_rex = next(
        system for system in ruleset_config.systems.values()
        if any(planet.system_id == system.id and planet.name == "Mecatol Rex" for planet in ruleset_config.planets.values())
    )
    assert mecatol_rex.back_color is None

def test_every_other_real_system_has_a_back_color(ruleset_config) -> None:
    mecatol_rex_system_ids = {
        planet.system_id for planet in ruleset_config.planets.values() if planet.name == "Mecatol Rex"
    }
    for system in ruleset_config.systems.values():
        if system.id not in mecatol_rex_system_ids and not system.is_off_board:
            assert system.back_color is not None, f"{system.id} has no back_color but isn't Mecatol Rex or off-board"

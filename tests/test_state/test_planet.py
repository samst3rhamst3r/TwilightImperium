"""Tests for app.state.planet.PlanetState."""
import pytest

from app.state.base.ownable import AlreadyOwnedResourceException, NotYetOwnedResourceException
from app.state.planet import PlanetState

@pytest.fixture
def planet_factory():
    def _make(**overrides) -> PlanetState:
        defaults = {"config_id": "mecatol_rex"}
        return PlanetState(**(defaults | overrides))
    return _make

def test_planet_state_defaults_to_uncontrolled_and_not_exhausted(planet_factory) -> None:
    planet = planet_factory()
    assert not planet.is_controlled
    assert planet.exhausted is False

def test_assign_control(planet_factory) -> None:
    planet = planet_factory()
    planet.assign_control("red")
    assert planet.is_controlled
    assert planet.is_controlled_by_player("red")

def test_assign_control_when_already_controlled_raises(planet_factory) -> None:
    planet = planet_factory()
    planet.assign_control("red")
    with pytest.raises(AlreadyOwnedResourceException):
        planet.assign_control("blue")

def test_reassign_control_swaps_controller(planet_factory) -> None:
    planet = planet_factory()
    planet.assign_control("red")
    released = planet.reassign_control("blue")
    assert released == "red"
    assert planet.is_controlled_by_player("blue")

def test_release_control_when_uncontrolled_raises(planet_factory) -> None:
    planet = planet_factory()
    with pytest.raises(NotYetOwnedResourceException):
        planet.release_control()

def test_planet_exhaust_and_ready(planet_factory) -> None:
    planet = planet_factory()
    planet.exhaust()
    assert planet.exhausted is True
    planet.ready()
    assert planet.exhausted is False

def test_planet_state_save_load_round_trip(planet_factory, declared_immutable_field_violations) -> None:
    planet = planet_factory(config_id="mecatol_rex")
    planet.assign_control("red")
    planet.exhaust()

    reloaded = PlanetState.load(planet.save())

    assert reloaded.config_id == "mecatol_rex"
    assert reloaded.is_controlled_by_player("red")
    assert reloaded.exhausted is True
    assert not declared_immutable_field_violations(reloaded)

"""Tests for app.state.special_tokens - the faction-gated and always-present
special token State classes."""
import pytest

from app.config.objs.system import WormholeType
from app.state.special_tokens import (
    CreussWormholeTokenState,
    CustodiansTokenState,
    InvalidWormholeType,
    NaaluTokenState,
    NekroAssimilatorTokenState,
    SpeakerTokenState,
)

# --- NaaluTokenState (plain PlayerOwnableMixin - no convenience forwarding;
# reached through .ownable directly) ---

def test_naalu_token_state_starts_unowned() -> None:
    assert not NaaluTokenState().ownable.is_owned

def test_naalu_token_state_set_and_release_owner() -> None:
    token = NaaluTokenState()
    token.ownable.set_owner("red")
    assert token.ownable.is_owned_by_player("red")
    assert token.ownable.release_owner() == "red"

def test_naalu_token_state_save_load_round_trip() -> None:
    token = NaaluTokenState()
    token.ownable.set_owner("red")
    reloaded = NaaluTokenState.load(token.save())
    assert reloaded.ownable.is_owned_by_player("red")

# --- SpeakerTokenState (bespoke "speaker" vocabulary) ---

def test_speaker_token_state_starts_with_no_speaker() -> None:
    token = SpeakerTokenState()
    assert token.speaker_player_id is None
    assert not token.is_player_speaker("red")

def test_speaker_token_state_assign_speaker() -> None:
    token = SpeakerTokenState()
    assert not token.is_speaker_assigned
    token.assign_speaker("red")
    assert token.is_speaker_assigned
    assert token.is_player_speaker("red")

def test_speaker_token_state_assign_speaker_overwrites_an_existing_speaker() -> None:
    """assign_speaker forwards to the now-unconditional _PlayerOwnable.set_owner
    - no dedicated reassign_speaker method anymore (that method was removed
    along with _PlayerOwnable.reassign_owner); assigning again just overwrites."""
    token = SpeakerTokenState()
    token.assign_speaker("red")
    token.assign_speaker("blue")
    assert token.is_player_speaker("blue")
    assert not token.is_player_speaker("red")

def test_speaker_token_state_release_speaker() -> None:
    token = SpeakerTokenState()
    token.assign_speaker("red")
    assert token.release_speaker() == "red"
    assert token.speaker_player_id is None

def test_speaker_token_state_save_load_round_trip() -> None:
    token = SpeakerTokenState()
    token.assign_speaker("red")
    reloaded = SpeakerTokenState.load(token.save())
    assert reloaded.speaker_player_id == "red"

# --- NekroAssimilatorTokenState ---

def test_nekro_assimilator_token_state_is_config_identified_and_starts_inactive() -> None:
    token = NekroAssimilatorTokenState(config_id="valefar_assimilator_x")
    assert token.id == "valefar_assimilator_x"
    assert not token.is_active

def test_nekro_assimilator_token_state_assimilate_and_reset() -> None:
    token = NekroAssimilatorTokenState(config_id="valefar_assimilator_x")
    token.assimilate_faction_tech_id("some_faction_tech")
    assert token.is_active
    assert token.assimilated_faction_tech_id == "some_faction_tech"
    token.reset()
    assert not token.is_active

def test_nekro_assimilator_token_state_save_load_round_trip() -> None:
    token = NekroAssimilatorTokenState(config_id="valefar_assimilator_y")
    token.assimilate_faction_tech_id("some_faction_tech")

    reloaded = NekroAssimilatorTokenState.load(token.save())

    assert reloaded.config_id == "valefar_assimilator_y"
    assert reloaded.assimilated_faction_tech_id == "some_faction_tech"

# --- CreussWormholeTokenState ---

def test_creuss_wormhole_token_state_accepts_alpha_and_beta() -> None:
    assert CreussWormholeTokenState(wormhole_type=WormholeType.ALPHA).wormhole_type is WormholeType.ALPHA
    assert CreussWormholeTokenState(wormhole_type=WormholeType.BETA).wormhole_type is WormholeType.BETA

def test_creuss_wormhole_token_state_rejects_delta() -> None:
    with pytest.raises(InvalidWormholeType):
        CreussWormholeTokenState(wormhole_type=WormholeType.DELTA)

def test_creuss_wormhole_token_state_save_load_round_trip() -> None:
    token = CreussWormholeTokenState(wormhole_type=WormholeType.ALPHA)

    reloaded = CreussWormholeTokenState.load(token.save())

    assert reloaded.wormhole_type is WormholeType.ALPHA
    assert reloaded.active_system_id is None

# --- CustodiansTokenState ---

def test_custodians_token_state_defaults_to_on_mecatol_rex() -> None:
    assert CustodiansTokenState().is_on_mecatol_rex is True

def test_custodians_token_state_save_load_round_trip() -> None:
    token = CustodiansTokenState(is_on_mecatol_rex=False)
    reloaded = CustodiansTokenState.load(token.save())
    assert reloaded.is_on_mecatol_rex is False

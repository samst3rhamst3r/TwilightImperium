"""Targeted regression tests for bugs fixed in the initial State-layer
remediation pass. Each test exists to catch re-introduction of one specific
bug - NOT a full per-class behavior suite (future work; mirroring
test_config's per-class test modules is a separate, larger undertaking).
"""
from app.config.objs.system import WormholeType
from app.config.player_color import PlayerColor
from app.geometry import HexCoordinate
from app.state.card.action import ActionCardState
from app.state.card.deck import CardDeckState
from app.state.card.promissory_note import PromissoryNoteCardState
from app.state.player import PlayerState
from app.state.special_tokens import CreussWormholeTokenState
from app.state.system import SystemState
from app.state.unit.unit import UnitState

def test_unit_state_save_load_round_trip():
    unit = UnitState(config_id="infantry")
    unit.place_on_planet("mecatol_rex")
    unit.take_hit()

    reloaded = UnitState.load(unit.save())

    assert reloaded.config_id == unit.config_id
    assert reloaded.instance_id == unit.instance_id
    assert reloaded.current_damage == 1
    assert reloaded.location.loc_type is unit.location.loc_type
    assert reloaded.location.unit_id == "mecatol_rex"

def test_system_state_save_load_round_trip():
    system = SystemState(config_id="sys_18", map_hex_coordinate=HexCoordinate(1, -1))

    reloaded = SystemState.load(system.save())

    assert reloaded.config_id == "sys_18"
    assert reloaded.map_hex_coordinate == HexCoordinate(1, -1)

def test_card_deck_state_save_load_round_trip_with_action_cards():
    card_a = ActionCardState(config_id="direct_hit", flavor_text_index=0)
    card_b = ActionCardState(config_id="sabotage", flavor_text_index=1)
    deck = CardDeckState(deck=[card_a, card_b], discard_pile=[])

    reloaded = CardDeckState.load(deck.save())

    assert [c.config_id for c in reloaded.deck] == ["direct_hit", "sabotage"]
    assert all(isinstance(c, ActionCardState) for c in reloaded.deck)
    assert reloaded.discard_pile == []

def test_player_state_command_token_pool_receive_and_remove():
    player = PlayerState(color=PlayerColor.RED, name="Sam", faction_id="sol")
    starting_pool = player.command_token_reinforcement_pool

    player.receive_command_tokens(2)
    assert player.command_token_reinforcement_pool == starting_pool + 2

    player.remove_from_command_token_pool(3)
    assert player.command_token_reinforcement_pool == starting_pool - 1

def test_promissory_note_state_save_load_round_trip_when_unissued():
    """Catches a bug found during remediation verification: init_from_save
    unconditionally called PlayerColor(data["issuing_player_color"]), which
    crashed on the legitimate None case (a note not yet issued to anyone)."""
    note = PromissoryNoteCardState(config_id="trade_agreement")
    assert note.issuing_player_color is None

    reloaded = PromissoryNoteCardState.load(note.save())

    assert reloaded.issuing_player_color is None
    assert not reloaded.is_issued_to_player

def test_creuss_wormhole_token_state_save_load_round_trip():
    token = CreussWormholeTokenState(wormhole_type=WormholeType.ALPHA)

    reloaded = CreussWormholeTokenState.load(token.save())

    assert reloaded.wormhole_type is WormholeType.ALPHA
    assert reloaded.active_system_id is None

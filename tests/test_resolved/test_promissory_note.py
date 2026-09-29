"""Tests for app.resolved.promissory_note.ResolvedPromissoryNote."""
import pytest

from app.config.player_color import PlayerColor
from app.config.ruleset_config import RulesetConfig
from app.resolved.promissory_note import ResolvedPromissoryNote
from app.state.card.promissory_note import PromissoryNoteCardState

def test_standard_note_renders_the_issuing_color_between_segments(ruleset_config: RulesetConfig) -> None:
    config = ruleset_config.promissory_notes["trade_agreement"]
    state = PromissoryNoteCardState(config_id="trade_agreement", issuing_player_color=PlayerColor.RED)

    text = ResolvedPromissoryNote(state, config).functional_text

    assert text == " red ".join(config.player_color_functional_text)
    assert text.startswith("When the red player")
    assert text.count("red") == len(config.player_color_functional_text) - 1

def test_faction_note_renders_its_fixed_text(ruleset_config: RulesetConfig) -> None:
    config = ruleset_config.promissory_notes["military_support"]
    state = PromissoryNoteCardState(config_id="military_support")

    assert ResolvedPromissoryNote(state, config).functional_text == config.functional_text

def test_standard_note_without_an_issuing_color_is_rejected(ruleset_config: RulesetConfig) -> None:
    state = PromissoryNoteCardState(config_id="trade_agreement")
    with pytest.raises(ValueError):
        ResolvedPromissoryNote(state, ruleset_config.promissory_notes["trade_agreement"])

def test_faction_note_with_an_issuing_color_is_rejected(ruleset_config: RulesetConfig) -> None:
    state = PromissoryNoteCardState(config_id="military_support", issuing_player_color=PlayerColor.BLUE)
    with pytest.raises(ValueError):
        ResolvedPromissoryNote(state, ruleset_config.promissory_notes["military_support"])

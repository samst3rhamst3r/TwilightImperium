"""Mirrors src/app/config/objs/promissory_note.py."""
import pytest

from app.config.objs.promissory_note import PromissoryNoteConfig
from app.config.shared import CanHaveFactionExclusivity, NamedConfigObj, RequiresFunctionalText

def test_promissory_note_config_composes_the_expected_mixins() -> None:
    assert issubclass(PromissoryNoteConfig, NamedConfigObj)
    assert issubclass(PromissoryNoteConfig, CanHaveFactionExclusivity)
    assert issubclass(PromissoryNoteConfig, RequiresFunctionalText)

def test_faction_exclusive_note_cannot_contain_the_player_color_placeholder() -> None:
    with pytest.raises(ValueError):
        PromissoryNoteConfig(
            id="x", name="X", faction_exclusive_id="sol",
            functional_text=f"Give this to {PromissoryNoteConfig.PLAYER_COLOR_REPLACE_STRING}.",
        )

def test_non_exclusive_note_may_contain_the_player_color_placeholder() -> None:
    note = PromissoryNoteConfig(
        id="x", name="X", functional_text=f"Give this to {PromissoryNoteConfig.PLAYER_COLOR_REPLACE_STRING}.",
    )
    assert PromissoryNoteConfig.PLAYER_COLOR_REPLACE_STRING in note.functional_text

def test_real_faction_exclusive_notes_never_contain_the_placeholder(ruleset_config) -> None:
    for note in ruleset_config.promissory_notes.values():
        if note.is_faction_exclusive:
            assert PromissoryNoteConfig.PLAYER_COLOR_REPLACE_STRING not in note.functional_text

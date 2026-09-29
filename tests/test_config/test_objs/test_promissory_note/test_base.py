"""Mirrors src/app/config/objs/promissory_note/base.py."""
from app.config.objs.named import NamedConfigObj
from app.config.objs.promissory_note import (
    FactionPromissoryNoteConfig,
    PromissoryNoteConfig,
    StandardPromissoryNoteConfig,
)

def test_promissory_note_config_is_a_named_config_obj() -> None:
    assert issubclass(PromissoryNoteConfig, NamedConfigObj)

def test_both_variants_share_the_base() -> None:
    assert issubclass(StandardPromissoryNoteConfig, PromissoryNoteConfig)
    assert issubclass(FactionPromissoryNoteConfig, PromissoryNoteConfig)

def test_variants_are_mutually_exclusive() -> None:
    """A note is either a standard (per-color) note or a faction note -
    never both, which is what the subclass split replaced the old
    `__PLAYER_COLOR__` placeholder string check with."""
    assert not issubclass(StandardPromissoryNoteConfig, FactionPromissoryNoteConfig)
    assert not issubclass(FactionPromissoryNoteConfig, StandardPromissoryNoteConfig)

def test_every_real_note_is_exactly_one_concrete_variant(ruleset_config) -> None:
    for note in ruleset_config.promissory_notes.values():
        assert type(note) in (StandardPromissoryNoteConfig, FactionPromissoryNoteConfig), (
            f"{note.id} loaded as bare {type(note).__name__}"
        )

"""Mirrors src/app/config/objs/action_card.py."""
from app.config.objs.action_card import ActionCardConfig
from app.config.shared import NamedConfigObj, RequiresFlavorTextOptions, RequiresFunctionalText

def test_action_card_config_composes_the_expected_mixins() -> None:
    assert issubclass(ActionCardConfig, NamedConfigObj)
    assert issubclass(ActionCardConfig, RequiresFunctionalText)
    assert issubclass(ActionCardConfig, RequiresFlavorTextOptions)

def test_num_in_deck_defaults_to_one() -> None:
    card = ActionCardConfig(id="x", name="X", functional_text="...", flavor_text_options=())
    assert card.num_in_deck == 1

def test_real_action_card_data_has_a_positive_num_in_deck(ruleset_config) -> None:
    for action_card in ruleset_config.action_cards.values():
        assert action_card.num_in_deck >= 1

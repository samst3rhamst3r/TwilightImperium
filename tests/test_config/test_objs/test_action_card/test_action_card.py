"""Mirrors src/app/config/objs/action_card/action_card.py."""
from app.config.objs.action_card import ActionCardConfig
from app.config.objs.mixins import RequiresFunctionalText
from app.config.objs.named import NamedConfigObj

def test_action_card_config_composes_the_expected_mixins() -> None:
    assert issubclass(ActionCardConfig, NamedConfigObj)
    assert issubclass(ActionCardConfig, RequiresFunctionalText)

def test_num_in_deck_defaults_to_one() -> None:
    card = ActionCardConfig(id="x", name="X", functional_text="...", flavor_text_options=())
    assert card.num_in_deck == 1

def test_from_dict_converts_flavor_text_options_to_a_tuple() -> None:
    card = ActionCardConfig.from_dict(
        {"id": "x", "name": "X", "functional_text": "...", "flavor_text_options": ["a", "b"]}
    )
    assert card.flavor_text_options == ("a", "b")

def test_real_action_card_data_has_a_positive_num_in_deck(ruleset_config) -> None:
    for action_card in ruleset_config.action_cards.values():
        assert action_card.num_in_deck >= 1

def test_real_action_card_data_always_has_flavor_text_options(ruleset_config) -> None:
    for action_card in ruleset_config.action_cards.values():
        assert action_card.flavor_text_options, f"{action_card.id} has no flavor_text_options"

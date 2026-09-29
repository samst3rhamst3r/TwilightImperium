"""Mirrors src/app/config/setup/loader.py."""
import pytest

from app.config.setup import SetupConfig, load_setup_data

@pytest.mark.parametrize("num_players", [3, 4, 5, 6])
def test_load_setup_data_returns_the_matching_player_count(data_dir, num_players: int) -> None:
    setup = load_setup_data(data_dir, num_players)
    assert isinstance(setup, SetupConfig)
    assert setup.num_players == num_players

@pytest.mark.parametrize("num_players", [2, 7])
def test_load_setup_data_rejects_unsupported_player_counts(data_dir, num_players: int) -> None:
    with pytest.raises(ValueError):
        load_setup_data(data_dir, num_players)

def test_real_setup_data_has_one_variant_per_player_count(data_dir) -> None:
    """load_setup_data returns the *first* match, so a duplicated player
    count in setup.yaml would silently shadow the later entry."""
    from app.config.yaml_loader import load_data
    counts = [len(entry["player_setup"]) for entry in load_data(data_dir / "setup" / "setup.yaml")]
    assert sorted(counts) == [3, 4, 5, 6]

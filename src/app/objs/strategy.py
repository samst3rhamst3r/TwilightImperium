
import pathlib, yaml

from ..game.exceptions import DiplomacyPrimaryAbilitytException, StrategyCardInitException
from .exhaustable import Exhaustable

_LEADERSHIP_PRIM_ABILITY_GAIN_TOKENS = 3
_LEADERSHIP_SEC_ABILITY_INFL_PER_TOKEN = 3

def _leadership_primary(player, influence: int = 0):
    player.gain_command_tokens( _LEADERSHIP_PRIM_ABILITY_GAIN_TOKENS )
    _leadership_secondary(player, influence)

def _leadership_secondary(player, influence: int):
    command_tokens = influence // _LEADERSHIP_SEC_ABILITY_INFL_PER_TOKEN
    player.gain_command_tokens(command_tokens)

def _diplomacy_primary(player, other_players, system):
    
    if player.has_planets(system.planets):
        raise DiplomacyPrimaryAbilitytException('Player does not control any planet in this system.')
    
    for other_player in other_players:
        other_player.place_command_token(system)
    
    for planet in system.planets:
        if planet in player.planets:
            player.ready_planet(planet)

def _diplomacy_secondary():
    pass

def _politics_primary():
    pass

def _politics_secondary():
    pass

def _construction_primary():
    pass

def _construction_secondary():
    pass

def _trade_primary():
    pass

def _trade_secondary():
    pass

def _warfare_primary():
    pass

def _warfare_secondary():
    pass

def _technology_primary():
    pass

def _technology_secondary():
    pass

def _imperial_primary():
    pass

def _imperial_secondary():
    pass

_ABILITY_MAPPING = {
    'Leadership': {
        'prim_ability': _leadership_primary, 
        'sec_ability': _leadership_secondary
        },
    'Diplomacy': {
        'prim_ability': _diplomacy_primary, 
        'sec_ability': _diplomacy_secondary
        },
    'Politics': {
        'prim_ability': _politics_primary, 
        'sec_ability': _politics_secondary
        },
    'Construction': {
        'prim_ability': _construction_primary, 
        'sec_ability': _construction_secondary
        },
    'Trade': {
        'prim_ability': _trade_primary, 
        'sec_ability': _trade_secondary
        },
    'Warfare': {
        'prim_ability': _warfare_primary, 
        'sec_ability': _warfare_secondary
        },
    'Technology': {
        'prim_ability': _technology_primary, 
        'sec_ability': _technology_secondary
        },
    'Imperial': {
        'prim_ability': _imperial_primary, 
        'sec_ability': _imperial_secondary
        },
}

class Strategy(Exhaustable):

    @classmethod
    def Init(cls, *, strategy_cards: dict | None = None, yaml_file_path: str | pathlib.Path | None = None):

        if strategy_cards is yaml_file_path is None:
            raise StrategyCardInitException('strategy_cards OR yaml_file_path must be defined')
        
        if strategy_cards is None:
            path = pathlib.Path(yaml_file_path).absolute()
            with open(path) as yaml_file:
                strategy_cards = yaml.safe_load(yaml_file)
        
        return {card['name']: cls(**card, **_ABILITY_MAPPING[card['name']]) for card in strategy_cards}


    def __init__(self, name: str, initiative: int, prim_ability: callable, sec_ability: callable, exhausted: bool = False) -> None:
        super().__init__(exhausted)
        
        self._name = name
        self._initiative = initiative
        self._prim_ability = prim_ability
        self._sec_ability = sec_ability
    
    @property
    def name(self):
        return self._name
    
    @property
    def initiative(self):
        return self._initiative
    
    def exec_prim_ability(self, *args, **kwargs):
        self._exhausted = True
        return self._prim_ability(*args, **kwargs)
    
    def exec_sec_ability(self, *args, **kwargs):
        return self._sec_ability(*args, **kwargs)
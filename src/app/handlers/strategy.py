from collections.abc import Iterable

class StrategyAbilityHandlerException(Exception): ...
class DiplomacyPrimaryAbilityHandlerException(StrategyAbilityHandlerException): ...
class DiplomacySecondaryAbilityHandlerException(StrategyAbilityHandlerException): ...

_LEADERSHIP_PRIM_ABILITY_GAIN_TOKENS = 3
_LEADERSHIP_SEC_ABILITY_INFL_PER_TOKEN = 3

def _leadership_primary(player, influence: int = 0) -> None:
    player.gain_command_tokens( _LEADERSHIP_PRIM_ABILITY_GAIN_TOKENS )
    _leadership_secondary(player, influence)

def _leadership_secondary(player, influence: int) -> None:
    command_tokens = influence // _LEADERSHIP_SEC_ABILITY_INFL_PER_TOKEN
    player.gain_command_tokens(command_tokens)

def _diplomacy_primary(player, other_players, system):
    
    if system.has_planet('Mecatol Rex'):
        raise DiplomacyPrimaryAbilityHandlerException('Cannot choose the Mecatol Rex system for the Primary Diplomacy ability.')
    
    controls_planet = False
    for planet in system.planets:
        if player.has_planet(planet):
            controls_planet = True
            break
    if not controls_planet:
        raise DiplomacyPrimaryAbilityHandlerException('Player does not control any planet in this system.')
    
    for other_player in other_players:
        other_player.place_command_token(system)
    
    for planet in system.planets:
        if planet in player.planets:
            player.ready_planet(planet)

def _diplomacy_secondary(player, planets: Iterable):
    player.spend_command_tokens(1)
    for planet in planets:
        player.ready_planet(planet)  # type: ignore

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

STRATEGY_CARD_ABILITY_HANDLER = {
    'leadership': {
        'prim_ability': _leadership_primary, 
        'sec_ability': _leadership_secondary
        },
    'diplomacy': {
        'prim_ability': _diplomacy_primary, 
        'sec_ability': _diplomacy_secondary
        },
    'politics': {
        'prim_ability': _politics_primary, 
        'sec_ability': _politics_secondary
        },
    'construction': {
        'prim_ability': _construction_primary, 
        'sec_ability': _construction_secondary
        },
    'trade': {
        'prim_ability': _trade_primary, 
        'sec_ability': _trade_secondary
        },
    'warfare': {
        'prim_ability': _warfare_primary, 
        'sec_ability': _warfare_secondary
        },
    'technology': {
        'prim_ability': _technology_primary, 
        'sec_ability': _technology_secondary
        },
    'imperial': {
        'prim_ability': _imperial_primary, 
        'sec_ability': _imperial_secondary
        },
}


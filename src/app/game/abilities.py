
import re, functools

def bombardment():
    pass

def sustain_damage(unit):
    unit.dmg_sustained = True

def anti_fighter_barrage():
    pass

def planetary_shield():
    pass

def space_cannon():
    pass

def production():
    pass

class Ability:

    _ABILITY_REGEX = re.compile(r'^(?P<func>([a-zA-Z]|-|\s)+)( (?P<level>(\d+|[xX]))( \(x(?P<dice>\d+)\))?)?$')

    _FUNC_MAP = {
        'anti-fighter barrage': anti_fighter_barrage,
        'bombardment': bombardment,
        'planetary shield': planetary_shield,
        'production': production, # Need to figure out 'PRODUCTION X' for Space Docks
        'space cannon': space_cannon,
        'sustain damage': sustain_damage
    }

    @classmethod
    def Create(cls, ability_str: str):
        
        match = cls._ABILITY_REGEX.match(ability_str)
        
        func = match.group('func').lower()
        level = match.group('level')
        dice = match.group('dice')

        args = {}
        if level is not None and level.isdigit():
            args['level'] = int(level)
        if dice is not None:
            args['dice'] = int(dice)

        return functools.partial(cls._FUNC_MAP[func], **args)
    
    def __init__(self, partial_func: callable):
        self._func = partial_func
    
    def __call__(self, *args, **kwds):
        return self._func(*args, **kwds)

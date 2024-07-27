import dataclasses as dc

@dc.dataclass(slots=True)
class Faction:
    name: str
    max_commodities: int    
    units: list | None = None
    techs: list | None = None
    home_systems: tuple | None = None

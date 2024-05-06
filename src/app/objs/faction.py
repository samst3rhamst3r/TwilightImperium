import dataclasses as dc

@dc.dataclass(slots=True)
class Faction:
    name: str
    units: list | None = None
    techs: list | None = None
    planets: list | None = None
    commodities: int = 0
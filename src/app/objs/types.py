from typing import TypeVar

type Faction = Faction
type Planet = Planet
type Player = Player

NamedObjType = TypeVar('NamedObjType', Faction, Planet, Player)

type StrNameOrNamedObjType = str | NamedObjType

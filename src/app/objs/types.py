from typing import TypeVar, TypeAlias

Faction: TypeAlias = "Faction"
Planet: TypeAlias = "Planet"
Player: TypeAlias = "Player"

NamedObjType = TypeVar('NamedObjType', Faction, Planet, Player)

type StrNameOrNamedObjType = str | NamedObjType

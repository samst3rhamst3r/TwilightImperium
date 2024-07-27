
from typing import Iterable, Any

class Player:

    def __init__(self, name: str, planets: Iterable | None = None) -> None:
        self._name = name

        if planets is None:
            self._planets = set()
        else:
            self._planets = set(planets)
    
    def gain_planets(self, planets: Iterable[Any]) -> None:
        self._planets.update(planets)

    def has_planets(self, planets: Iterable[Any]) -> bool:
        return self._planets.issuperset(planets)
    
    def has_planet(self, planet) -> bool:
        return planet in self._planets
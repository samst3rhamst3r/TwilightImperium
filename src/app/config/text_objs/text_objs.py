from dataclasses import dataclass

from .base import BaseTextConfigObj, OnlyFunctionalTextConfig, FunctionalWithFlavorTextOptionsConfig, OnlyFlavorTextConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityCardTextConfig(OnlyFunctionalTextConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class ActionCardTextConfig(FunctionalWithFlavorTextOptionsConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class AgendaTextConfig(OnlyFunctionalTextConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class ObjectiveCardTextConfig(OnlyFunctionalTextConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class PlanetTextConfig(OnlyFlavorTextConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteTextConfig(OnlyFunctionalTextConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyTextConfig(BaseTextConfigObj):
    primary_ability_text: str
    secondary_ability_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class TechTextConfig(OnlyFunctionalTextConfig):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitTextConfig(OnlyFunctionalTextConfig):
    pass

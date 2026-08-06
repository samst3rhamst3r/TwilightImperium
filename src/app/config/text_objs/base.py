from dataclasses import dataclass

from app.config.shared import IDConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseTextConfigObj(IDConfigObj):
    """Base class for all text configurations. Used by type-checkers."""
    pass

@dataclass(frozen=True, frozen=True, kw_only=True)
class RequiresFunctionalText:
    functional_text: str

@dataclass(frozen=True, frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: tuple[str, ...]

@dataclass(frozen=True, frozen=True, kw_only=True)
class RequiresFlavorText:
    flavor_text: str

############## DERIVED CLASSES - SUB-CLASSED BY MOST GAME TEXT-CONFIG OBJECTS

@dataclass(frozen=True, frozen=True, kw_only=True)
class OnlyFunctionalTextConfig(BaseTextConfigObj, RequiresFunctionalText):
    pass

@dataclass(frozen=True, frozen=True, kw_only=True)
class FunctionalWithFlavorTextOptionsConfig(OnlyFunctionalTextConfig, RequiresFlavorTextOptions):
    pass

@dataclass(frozen=True, frozen=True, kw_only=True)
class OnlyFlavorTextConfig(BaseTextConfigObj, RequiresFlavorText):
    pass




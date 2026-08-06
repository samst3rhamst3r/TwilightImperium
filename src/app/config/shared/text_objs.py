from dataclasses import dataclass

@dataclass(frozen=True, frozen=True, kw_only=True)
class RequiresFunctionalText:
    functional_text: str

@dataclass(frozen=True, frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: tuple[str, ...]

@dataclass(frozen=True, frozen=True, kw_only=True)
class RequiresFlavorText:
    flavor_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class PrimarySecondaryAbilityTextConfig:
    primary_ability_text: str
    secondary_ability_text: str

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
class CanHaveFactionExclusivity:
    faction_exclusive_id: str | None = None

    @property
    def is_faction_exclusive(self) -> bool:
        return self.faction_exclusive_id is not None

    def is_exclusive_to(self, faction_id: str) -> bool:
        return self.faction_exclusive_id == faction_id

@dataclass(slots=True, frozen=True, kw_only=True)
class CanBeExhaustable:
    exhaustable: bool = False

@dataclass(slots=True, frozen=True, kw_only=True)
class IsExhaustable(CanBeExhaustable):

    def __post_init__(self):
        super().__post_init__()
        self.exhaustable = True

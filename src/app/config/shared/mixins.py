from dataclasses import dataclass

# NOTE: these mixins are deliberately NOT slots=True - and neither is any
# other Config dataclass (see ARCHITECTURE.md §2). CPython's multiple
# inheritance only tolerates one base class in the MRO contributing real
# (non-empty) __slots__, so combining two or more slotted mixins raises
# "TypeError: multiple bases have instance lay-out conflict" at
# class-definition time. Slotting only some classes in a hierarchy doesn't
# even buy anything - the instance still gets a __dict__ the moment any
# class in its MRO lacks __slots__ - so once mixin composition ruled out
# slotting everything, omitting slots=True everywhere was the only
# configuration that's both correct and consistent.

@dataclass(frozen=True, kw_only=True)
class RequiresFunctionalText:
    functional_text: str

@dataclass(frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: tuple[str, ...]

@dataclass(frozen=True, kw_only=True)
class RequiresFlavorText:
    flavor_text: str

@dataclass(frozen=True, kw_only=True)
class CanHaveFactionExclusivity:
    faction_exclusive_id: str | None = None

    @property
    def is_faction_exclusive(self) -> bool:
        return self.faction_exclusive_id is not None

    def is_exclusive_to(self, faction_id: str) -> bool:
        return self.faction_exclusive_id == faction_id

@dataclass(frozen=True, kw_only=True)
class CanBeExhaustible:
    exhaustible: bool = False

from dataclasses import dataclass

# NOTE: these mixins are deliberately NOT slots=True. CPython's multiple
# inheritance only tolerates one base class in the MRO contributing real
# (non-empty) __slots__; since concrete Config classes combine two or more of
# these mixins with NamedConfigObj/IDConfigObj (which *is* slotted), giving
# every mixin its own slots raises "TypeError: multiple bases have instance
# lay-out conflict" at class-definition time. These are tiny, load-once
# config objects - the __dict__ memory cost of leaving mixins unslotted is
# negligible next to correctness.

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

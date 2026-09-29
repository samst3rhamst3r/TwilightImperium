from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanBeExhaustible, CanHaveFactionExclusivity, RequiresFactionExclusivity, RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText):
    # No faction-exclusivity mixin here - whether it's required varies by
    # subclass (optional for a standard tech, mandatory for an Assimilator
    # token), so each subclass composes the mixin matching its own rule
    # rather than TechConfig picking one cardinality for both.
    # No CanBeExhaustible here either - only a standard tech is ever
    # exhausted; an Assimilator token isn't a real card in play.
    # No prereqs here either - an Assimilator token isn't upgraded through
    # the tech tree, so it has no prerequisites to speak of.
    pass

@dataclass(frozen=True, kw_only=True)
class StandardTechConfig(TechConfig, CanHaveFactionExclusivity, CanBeExhaustible, FromDictMixin):
    """A real technology - has a fixed tech_type from the moment it's drawn/owned.
    Faction exclusivity is optional here (most techs aren't faction-locked).
    The only TechConfig subclass with prereqs, and consequently the only one
    that needs coercion (nested TechUpgradeReqConfig, TechType) - hence the
    only one composing FromDictMixin."""
    tech_type: TechType
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["prereqs"] = tuple(TechUpgradeReqConfig.from_dict(req) for req in d.get("prereqs", ()))
        d["tech_type"] = TechType(d["tech_type"])

@dataclass(frozen=True, kw_only=True)
class AssimilatorTechConfig(TechConfig, RequiresFactionExclusivity):
    """Nekro Virus's Valefar Assimilator X/Y tokens (see TechID). These aren't a
    technology in their own right - they take on whatever tech_type the
    technology they assimilate has, so they carry no static tech_type of
    their own. Unlike a standard tech's optional exclusivity, these tokens
    are only ever printed for Nekro Virus, so faction_exclusive_id is
    mandatory (RequiresFactionExclusivity), not optional. Every field here
    (id, name, functional_text, faction_exclusive_id) is already a
    YAML-native primitive, so no coercion - and no FromDictMixin - is
    needed; plain construction from the raw dict is sufficient."""
    pass

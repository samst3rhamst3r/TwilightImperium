from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import CanBeExhaustible, RequiresFunctionalText
from app.config.objs.planet import PlanetTrait

from .type import AgendaType
from .vote_scenario_type import AgendaVoteScenarioType

@dataclass(frozen=True, kw_only=True)
class AgendaConfig(NamedConfigObj, RequiresFunctionalText, CanBeExhaustible):
    agenda_type: AgendaType
    vote_scenario_type: AgendaVoteScenarioType
    planet_trait: PlanetTrait | None = None

    def __post_init__(self):
        # object.__setattr__ is required here - the dataclass is frozen, so
        # plain attribute assignment (even from within __post_init__) raises
        # FrozenInstanceError. Same pattern RulesetConfig.__post_init__ uses
        # to wrap its dict fields in MappingProxyType after construction.
        object.__setattr__(self, "agenda_type", AgendaType(self.agenda_type))
        object.__setattr__(self, "vote_scenario_type", AgendaVoteScenarioType(self.vote_scenario_type))
        if self.planet_trait is not None and self.vote_scenario_type is not AgendaVoteScenarioType.ELECT_PLANET:
            raise ValueError("planet_trait is only allowed for ELECT_PLANET scenario")

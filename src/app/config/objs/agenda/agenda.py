from dataclasses import dataclass, field

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFunctionalText
from app.config.objs.planet import PlanetTrait

from .type import AgendaType
from .vote_scenario_type import AgendaVoteScenarioType

@dataclass(slots=True, frozen=True, kw_only=True)
class AgendaConfig(NamedConfigObj, RequiresFunctionalText):
    type_: AgendaType = field(metadata={"key": "type"})
    vote_scenario_type: AgendaVoteScenarioType
    planet_trait: PlanetTrait | None = None

    def __post_init__(self):
        if self.planet_trait is not None and self.vote_scenario_type is not AgendaVoteScenarioType.ELECT_PLANET:
            raise ValueError("planet_trait is only allowed for ELECT_PLANET scenario")

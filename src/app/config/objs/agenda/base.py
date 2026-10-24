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

    def __post_init__(self) -> None:
        if self.planet_trait is not None and self.vote_scenario_type is not AgendaVoteScenarioType.ELECT_PLANET:
            raise ValueError("planet_trait is only allowed for ELECT_PLANET scenario")
        
    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        d["agenda_type"] = AgendaType(d["agenda_type"])
        d["vote_scenario_type"] = AgendaVoteScenarioType(d["vote_scenario_type"])
        if d.get("planet_trait") is not None:
            d["planet_trait"] = PlanetTrait(d["planet_trait"])

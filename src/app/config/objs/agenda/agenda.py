from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanBeExhaustible, RequiresFunctionalText
from app.config.objs.planet import PlanetTrait

from .type import AgendaType
from .vote_scenario_type import AgendaVoteScenarioType

@dataclass(frozen=True, kw_only=True)
class AgendaConfig(NamedConfigObj, RequiresFunctionalText, CanBeExhaustible, FromDictMixin):
    agenda_type: AgendaType
    vote_scenario_type: AgendaVoteScenarioType
    planet_trait: PlanetTrait | None = None

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["agenda_type"] = AgendaType(d["agenda_type"])
        d["vote_scenario_type"] = AgendaVoteScenarioType(d["vote_scenario_type"])

        trait = d.get("planet_trait")
        if trait is not None:
            d["planet_trait"] = PlanetTrait(d["planet_trait"])

    def __post_init__(self) -> None:
        if self.planet_trait is not None and self.vote_scenario_type is not AgendaVoteScenarioType.ELECT_PLANET:
            raise ValueError("planet_trait is only allowed for ELECT_PLANET scenario")
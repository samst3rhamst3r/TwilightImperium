from enum import auto

from app.config.enum import ConfigEnum

class AgendaVoteScenarioType(ConfigEnum):
    FOR_AGAINST = auto()
    ELECT_PLAYER = auto()
    ELECT_PLANET = auto()
    ELECT_LAW = auto()
    ELECT_SCORED_SECRET_OBJECTIVE = auto()

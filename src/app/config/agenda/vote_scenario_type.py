import enum

class AgendaVoteScenarioType(enum.StrEnum):
    FOR_AGAINST = enum.auto()
    ELECT_PLAYER = enum.auto()
    ELECT_PLANET = enum.auto()
    ELECT_LAW = enum.auto()
    ELECT_SCORED_SECRET_OBJECTIVE = enum.auto()

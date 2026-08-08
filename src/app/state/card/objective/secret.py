from dataclasses import dataclass

from .base import ObjectiveCardState

@dataclass(slots=True, kw_only=True)
class SecretObjectiveCardState(ObjectiveCardState):
    scored: bool = False

    def to_save_dict(self):
        return super().to_save_dict() | {
            "scored": self.scored
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.scored = data["scored"]

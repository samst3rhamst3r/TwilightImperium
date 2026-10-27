from dataclasses import dataclass

from .base import InvalidStateTransition, ObjectiveCardState, Revealable

@dataclass(kw_only=True)
class PublicObjectiveCardState(ObjectiveCardState, Revealable):
    _revealed: bool = False

    @property
    def is_revealed(self) -> bool:
        return self._revealed

    def reveal(self) -> None:
        if self.is_revealed:
            raise InvalidStateTransition("This public objective is already revealed.")
        self._revealed = True

    def save(self):
        return super().save() | {
            "_revealed": self._revealed
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self._revealed = data["_revealed"]

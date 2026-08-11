from dataclasses import dataclass

from app.state.base.serializable import Serializable

class ExhaustibleAlreadyExhausted(Exception):
    pass

class ExhaustibleAlreadyReadied(Exception):
    pass

class ObjectNotExhaustible(Exception):
    pass

@dataclass(kw_only=True)
class Exhaustible(Serializable):
    exhausted: bool | None = None

    def save(self) -> dict:
        return super().save() | {
            "exhausted": self.exhausted
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.exhausted = data["exhausted"]

    @property
    def can_be_exhausted(self):
        return self.exhausted is not None

    def exhaust(self):
        """Exhaust the object."""
        if not self.can_be_exhausted:
            raise ObjectNotExhaustible('This object is not exhaustible.')
        if self.exhausted:
            raise ExhaustibleAlreadyExhausted('Cannot exhaust an already exhausted object.')
        self.exhausted = True
    
    def ready(self):
        """Ready the object."""
        if not self.can_be_exhausted:
            raise ObjectNotExhaustible('This object is not exhaustible.')
        if not self.exhausted:
            raise ExhaustibleAlreadyReadied('Cannot ready an already readied object.')
        self.exhausted = False

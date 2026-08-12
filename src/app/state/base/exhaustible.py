from dataclasses import dataclass

from app.state.base.serializable import Serializable

class ExhaustibleAlreadyExhausted(Exception):
    pass

class ExhaustibleAlreadyReadied(Exception):
    pass

@dataclass(kw_only=True)
class Exhaustible(Serializable):
    # Whether a class can be exhausted at all is a structural property of
    # composing this mixin, not a per-instance question - so `exhausted` is
    # a plain bool, never None (matching ARCHITECTURE.md section 2's
    # trait-split principle: don't use Optional for "this concept doesn't
    # apply here", the mixin's presence/absence already encodes that).
    exhausted: bool = False

    def save(self) -> dict:
        return super().save() | {
            "exhausted": self.exhausted
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.exhausted = data["exhausted"]

    def exhaust(self):
        """Exhaust the object."""
        if self.exhausted:
            raise ExhaustibleAlreadyExhausted('Cannot exhaust an already exhausted object.')
        self.exhausted = True

    def ready(self):
        """Ready the object."""
        if not self.exhausted:
            raise ExhaustibleAlreadyReadied('Cannot ready an already readied object.')
        self.exhausted = False

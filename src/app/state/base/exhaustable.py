from dataclasses import dataclass

from app.state.base.protocols import MixinInitializer, Savable

class ExhaustableAlreadyExhausted(Exception):
    pass

class ExhaustableAlreadyReadied(Exception):
    pass

@dataclass(slots=True, kw_only=True)
class Exhaustable(Savable, MixinInitializer):
    exhausted: bool = False

    def to_save_dict(self) -> dict:
        return {"exhausted": self.exhausted}

    def exhaust(self):
        """Exhaust the object."""
        if self.exhausted:
            raise ExhaustableAlreadyExhausted('Cannot exhaust an already exhausted object.')
        self.exhausted = True
    
    def ready(self):
        """Ready the object."""
        if not self.exhausted:
            raise ExhaustableAlreadyReadied('Cannot ready an already readied object.')
        self.exhausted = False
    
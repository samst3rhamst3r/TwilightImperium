
from ..game.exceptions import ExhaustableAlreadyExhausted

class Exhaustable:

    def __init__(self, exhausted: bool = False) -> None:
        self._exhausted = exhausted
    
    @property
    def exhausted(self):
        return self._exhausted
    
    def exhaust(self):
        if self.exhausted:
            raise ExhaustableAlreadyExhausted('Cannot exhaust an already exhausted object.')
        self._exhausted = True
    
    def ready(self):
        self._exhausted = False
    
from dataclasses import dataclass

class ExhaustableAlreadyExhausted(Exception):
    pass

@dataclass(slots=True, kw_only=True)
class Exhaustable:
    exhausted: bool = False
    
    def exhaust(self):
        if self.exhausted:
            raise ExhaustableAlreadyExhausted('Cannot exhaust an already exhausted object.')
        self.exhausted = True
    
    def ready(self):
        self.exhausted = False
    
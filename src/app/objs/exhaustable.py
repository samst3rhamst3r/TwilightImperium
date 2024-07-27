
class Exhaustable:

    def __init__(self, exhausted: bool = False) -> None:
        self._exhausted = exhausted
    
    @property
    def exhausted(self):
        return self._exhausted
    
    def exhaust(self):
        self._exhausted = True
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class HexCoordinate:
    q: int
    r: int

    @property
    def s(self):
        return -self.q - self.r

    def __str__(self):
        return f"({self.q},{self.r},{self.s})"
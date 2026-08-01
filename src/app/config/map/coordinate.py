from dataclasses import dataclass

from app.config.shared import BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class HexCoordinate(BaseConfigObj):
    q: int
    r: int

    @property
    def s(self):
        return -self.q - self.r

    def __str__(self):
        return f"({self.q},{self.r},{self.s})"
from dataclasses import dataclass

from typing import Self

@dataclass(slots=True, frozen=True)
class HexCoordinate:
    q: int
    r: int

    @property
    def s(self):
        return -self.q - self.r

    def __str__(self):
        return f"({self.q},{self.r},{self.s})"

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.q - other.q, self.r - other.r)
    
    @property
    def neighbors(self) -> tuple[Self]:
        return (
            self.__class__(self.q + 1, self.r - 1),
            self.__class__(self.q + 1, self.r),
            self.__class__(self.q, self.r + 1),
            self.__class__(self.q, self.r - 1),
            self.__class__(self.q - 1, self.r + 1),
            self.__class__(self.q - 1, self.r),
        )

    def distance_to(self, other: Self) -> int:
        return (abs(self.q - other.q) + abs(self.r - other.r) + abs(self.s - other.s)) // 2
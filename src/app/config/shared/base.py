from typing import Self

class BaseConfigObj:
    """Base class for all configuration objects."""

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        cls._parse_fields(d)
        return cls(**d)

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        ...

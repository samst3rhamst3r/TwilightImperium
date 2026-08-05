from typing import Protocol, Any, Self

class Savable(Protocol):
    def to_save_dict(self) -> dict[str, Any]: ...

class Loadable(Savable):
    @classmethod
    def from_save_dict(cls, **_) -> Self: ...

class MixinInitializer(Protocol):
    @staticmethod
    def init_from_save_dict(data: dict) -> None: ...
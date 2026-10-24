from typing import Protocol

from app.state.base.exhaustible import Exhaustible
from app.config.shared.mixins import CanBeExhaustible

class IncompatibleExhaustProtocolError(TypeError):
    pass

class IsExhaustibleProtocol(Protocol):
    state: Exhaustible

    @property
    def is_exhaustible(self) -> bool:
        return True

    @property
    def is_exhausted(self) -> bool:
        return self.state.exhausted

    def exhaust(self) -> None:
        self.state.exhaust()

    def ready(self) -> None:
        self.state.ready()

class CanBeExhaustibleProtocol(IsExhaustibleProtocol, Protocol):
    config: CanBeExhaustible

    def __post_init__(self) -> None:
        if not self.config.exhaustible and self.state.exhausted:
            raise IncompatibleExhaustProtocolError("Cannot initialize exhausted state to True with a non-exhaustible config.")

    def _validate(self) -> None:
        if not self.config.exhaustible:
            raise IncompatibleExhaustProtocolError("Cannot use exhaust protocol on a non-exhaustible object.")

    @property
    def is_exhaustible(self) -> bool:
        return self.config.exhaustible
    
    @property
    def is_exhausted(self) -> bool:
        self._validate()
        return super().is_exhausted

    def exhaust(self) -> None:
        self._validate()
        super().exhaust()

    def ready(self) -> None:
        self._validate()
        super().ready()
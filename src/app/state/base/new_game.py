from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(slots=True, kw_only=True)
class NewGameInitializable(ABC):

    @abstractmethod
    def initialize_new_game(self) -> None: ...

@dataclass(slots=True, kw_only=True)
class NewGameCreatable(NewGameInitializable):

    @abstractmethod
    def new_game(self, **kwargs) -> None: ...
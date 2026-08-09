from typing import Protocol, Self

class Savable(Protocol):
    """Protocol for objects that can be saved and re-initialized."""

    def save(self) -> dict:
        """It is recommended to implement this method in any dataclass that has savable fields, even
        if the data is primitive. By keeping the interface consistent, we can ensure that
        all saveable objects can be serialized and deserialized in a uniform manner.
        """
        raise NotImplementedError(f"The {self.__class__.__name__} class does not implement the 'save' method. Please implement it.")

    def init_from_save(self, data: dict) -> None:
        """This should get implemented in any subclass that has fields to initialize 
        after object creation via save data. Must be implemented if used as a mixin.
        Raises NotImplementedError otherwise.
        """
        raise NotImplementedError(f"The {self.__class__.__name__} class does not implement the 'init_from_save' method. Please implement it.")

class NewGameProtocol(Protocol):

    def init_new_game(self, **kwargs) -> None: ...

    @classmethod
    def new_game(cls, **kwargs) -> Self: 
        obj = cls.__new__(cls)
        obj.init_new_game(**kwargs)
        return obj

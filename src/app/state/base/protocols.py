from typing import Protocol, Self

class _Dumpable(Protocol):
    """Protocol that can be used in many objects to gather any saveable data.
    
    It is recommended to implement this in any dataclass that has savable fields, even
    if the data is primitive. By keeping the interface consistent, we can ensure that
    all saveable objects can be serialized and deserialized in a uniform manner.
    """

    def to_save_dict(self) -> dict:
        raise NotImplementedError(f"The {self.__class__.__name__} class does not implement the 'to_save_dict' method. Please implement it.")

class _Initializable(Protocol):
    """Protocol for objects that can be initialized from a save dictionary.

    This should get implemented in any subclass that has fields to initialize 
    after object creation via save data. Must be implemented if used as a mixin.
    Raises NotImplementedError otherwise.
    """
    def init_from_save(self, data: dict) -> None:
        raise NotImplementedError(f"The {self.__class__.__name__} class does not implement the 'init_from_save' method. Please implement it.")

class Savable(_Dumpable, _Initializable, Protocol):
    """Protocol for objects that can be saved and re-initialized.
    
    Useful for type-checkers.
    """

class Loadable(Savable, Protocol):
    """Protocol for objects that can be initialized from a save dictionary.
    Leaf classes should not need to override from_save_dict. Inheriting from Loadable
    should be enough to provide the boilerplate machinery.
    
    Sub classes would then implement just the Initializable portion (init_from_save)
    as the variable initialization portion specific to their class.
    """
    @classmethod
    def from_save_dict(cls, data: dict) -> Self:
        obj = cls.__new__(cls)
        obj.init_from_save(data)
        return obj

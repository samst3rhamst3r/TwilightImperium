from typing import Protocol, Self

class Savable(Protocol):
    """Protocol that can be used in many objects to gather any saveable data.
    
    It is recommended to implement this in any dataclass that has savable fields, even
    if the data is primitive. By keeping the interface consistent, we can ensure that
    all saveable objects can be serialized and deserialized in a uniform manner.
    """
    def to_save_dict(self) -> dict:
        return {}

class MixinInitializer(Protocol):
    """Provides a static method for initializing objects from a save dictionary.
    If a class requires specialized initialization logic beyond raw serializable values,
    it can override this method.

    It is recommended to inherit into any class that has savable fields even if there is
    no override, then to call this method from containing objects.
    """
    @staticmethod
    def init_from_save_dict(data: dict) -> dict:
        return data

class Loadable(MixinInitializer):
    """Protocol for objects that can be initialized from a save dictionary.
    Leaf classes are most likely the only ones to implement this.
    
    Super classes should implement the MixinInitializer instead, then have
    the leaf classes call the MixinInitializer method from this method to initialize the input
    dictionary.
    """
    @classmethod
    def from_save_dict(cls, input_dict: dict) -> Self:
        input_dict = cls.init_from_save_dict(input_dict)
        return cls(**input_dict)

from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class FromDictMixin:
    """Mixin class that provides a method to create an instance from a dictionary."""

    @classmethod
    def from_dict(cls, data: dict):
        """Create an instance of the class from a dictionary."""
        cls._init_from_dict(data)  # Call the subclass's _init_from_dict method
        return cls(**data)

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        raise NotImplementedError("Subclasses must implement _init_from_dict method.")
    
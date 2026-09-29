from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class FromDictMixin:
    """Mixin class that provides a method to create an instance from a dictionary."""

    @classmethod
    def from_dict(cls, data: dict):
        """Create an instance of the class from a dictionary.

        The caller's dict is never mutated - _init_from_dict works on a shallow
        copy. This matters for YAML anchors/aliases (e.g. `*combat_args` in
        abilities/parameterized.yaml), which safe_load resolves to the *same*
        dict object shared by every alias: converting it in place would hand
        already-converted values to the next entry that references it."""
        data = dict(data)
        cls._init_from_dict(data)  # Call the subclass's _init_from_dict method
        return cls(**data)

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        raise NotImplementedError("Subclasses must implement _init_from_dict method.")

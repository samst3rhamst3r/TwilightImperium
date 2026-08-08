from dataclasses import dataclass

from app.state.base.protocols import Loadable

@dataclass(kw_only=True)
class StateObj(Loadable):
    """Top-level class used for type-checkers and to provide a common interface for all state objects.
    The Loadable Protocol ends at this point by no longer calling super() in to_save_dict and
    init_from_save.
    """

    def to_save_dict(self) -> dict:
        return {}

    def init_from_save(self, _: dict) -> None:
        pass

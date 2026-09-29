from collections.abc import Iterable
from types import MappingProxyType

from .id import IDConfigObj

class DuplicateConfigIDError(ValueError):
    pass

def index_by_id[T: IDConfigObj](configs: Iterable[T]) -> MappingProxyType[str, T]:
    """Return a read-only mapping of config.id -> config for the given configs.

    Raises DuplicateConfigIDError rather than letting a later entry silently
    replace an earlier one with the same id."""
    index: dict[str, T] = {}
    for config in configs:
        if config.id in index:
            raise DuplicateConfigIDError(f"Duplicate config id {config.id!r}: {index[config.id]!r} and {config!r}")
        index[config.id] = config
    return MappingProxyType(index)

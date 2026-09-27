from collections.abc import Iterable
from types import MappingProxyType

from .id import IDConfigObj

def index_by_id[T: IDConfigObj](configs: Iterable[T]) -> MappingProxyType[str, T]:
    """Return a read-only mapping of config.id -> config for the given configs."""
    return MappingProxyType({config.id: config for config in configs})
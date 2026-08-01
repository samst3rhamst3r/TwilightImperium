from dataclasses import dataclass

from app.config.shared import BaseConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj[TConfig: BaseConfigObj]:
    """Base class for all state objects."""
    config: TConfig
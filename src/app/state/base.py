from dataclasses import dataclass
from typing import Final

from app.config.base import BaseConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj[TConfig: BaseConfigObj, TTextConfig: BaseTextConfigObj]:
    """Base class for all state objects."""
    config: Final[TConfig]
    text_config: Final[TTextConfig]
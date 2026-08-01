from dataclasses import dataclass, field
from typing import Final
from uuid import uuid4

from app.config.base import BaseConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj[TConfig: BaseConfigObj, TTextConfig: BaseTextConfigObj]:
    """Base class for all state objects."""
    config: Final[TConfig]
    text_config: Final[TTextConfig]
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)
    
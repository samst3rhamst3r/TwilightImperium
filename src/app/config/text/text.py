

from dataclasses import dataclass, field
from typing import Any, Optional

from app.config.shared import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseTextConfig(ConfigObj):
    _functional_text: Any = field(metadata={"key": "functional_text"})
    flavor_text: Optional[str] = None

    @property
    def functional_text(self) -> str:
        return self._functional_text

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseTextConfigWithFlavor(BaseTextConfig):
    flavor_text: Optional[str] = None
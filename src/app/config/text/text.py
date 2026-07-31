

from dataclasses import dataclass
from typing import Optional

from app.config.shared import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseTextObj(ConfigObj):
    functional_text: str
    flavor_text: Optional[str] = None
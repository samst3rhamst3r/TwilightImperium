from dataclasses import dataclass

from app.config.objs.named import NamedConfigObj

@dataclass(frozen=True, kw_only=True)
class PromissoryNoteConfig(NamedConfigObj):
    pass
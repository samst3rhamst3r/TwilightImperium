from dataclasses import dataclass

from config.objs.named import NamedConfigObj

@dataclass(frozen=True, kw_only=True)
class PromissoryNoteConfig(NamedConfigObj):
    pass
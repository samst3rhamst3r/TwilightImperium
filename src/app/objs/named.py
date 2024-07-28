
import dataclasses as dc

from .types import StrNameOrNamedObjType

@dc.dataclass(frozen=True, slots=True)
class NamedObject:
    name: str
    
    def __eq__(self, other: StrNameOrNamedObjType) -> bool:
        if isinstance(other, str):
            return self.name == other.name
        else:
            return self is other
        
    def __ne__(self, other: StrNameOrNamedObjType) -> bool:
        if isinstance(other, str):
            return self.name != other.name
        else:
            return self is not other
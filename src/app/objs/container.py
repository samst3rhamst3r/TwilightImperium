
from .types import NamedObjType, StrNameOrNamedObjType

class NamedObjectSequence[T: (list, tuple, set)]:

    def __init__(self, container: T[NamedObjType]) -> None:
        self._container = container
        self._iter = None

    def __contains__(self, item: StrNameOrNamedObjType) -> bool:
        
        if isinstance(item, str):
            for val in self._container:
                if val.name == item:
                    return True
        else:
            for val in self._container:
                if val is item:
                    return True
                
    def __iter__(self) -> NamedObjType:
        self._iter = iter(self._container)
        return self._iter
    
    def __next__(self) -> NamedObjType:
        return next(self._iter)

    def __len__(self) -> int:
        return len(self._container)
    
    def __del__(self, item: StrNameOrNamedObjType) -> None:
        if isinstance(item, str):
            for val in self._container:
                if val.name == item:
                    del self._container[val]
        else:
            del self._container[item]
    
    def __reversed__(self):
        return reversed(self._container)

    def __getitem__(self, key: StrNameOrNamedObjType) -> NamedObjType:
        if isinstance(key, str):
            for item in self._container:
                if item.name == key:
                    return item
        else:
            return self._container[key]
    
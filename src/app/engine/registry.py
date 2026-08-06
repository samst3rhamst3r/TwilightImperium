from app.config.shared import IDConfigObj

class Registry[T: IDConfigObj]:

    def __init__(self):
        self._items: dict[str, T] = {}

    def register(self, obj_: T):
        self._items[obj_.id] = obj_

    def get(self, key: str, *, raise_on_error: bool = True) -> T | None:
        if raise_on_error and key not in self._items:
            raise KeyError(f"'{type(T).__name__}' item with key '{key}' not found")
        return self._items.get(key)

from dataclasses import dataclass

from app.state.base import Serializable

@dataclass(kw_only=True)
class CustodiansTokenState(Serializable):
    is_on_mecatol_rex: bool = True

    def save(self) -> dict:
        return super().save() | {
            "is_on_mecatol_rex": self.is_on_mecatol_rex
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.is_on_mecatol_rex = data["is_on_mecatol_rex"]

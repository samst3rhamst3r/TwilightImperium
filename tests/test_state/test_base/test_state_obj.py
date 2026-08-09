from typing import Self

import pytest

from app.state.base.serializable import Serializable
from app.state.base.exhaustible import Exhaustible

class _Test_CompositeClasses(Serializable, Exhaustible):

    def save(self) -> dict:
        return super().save()

    def init_from_dict(self) -> None:
        pass

    @classmethod
    def new_game(cls, **kwargs) -> Self:
        return super().new_game(**kwargs)

def test_state_obj():
    _Test_CompositeClasses
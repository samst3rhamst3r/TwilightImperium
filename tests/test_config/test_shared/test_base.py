import pytest
from pathlib import Path

from app.config.shared import *

@pytest.fixture
def data_dir():
    return Path("data")

@pytest.fixture
def data_objs_dir(data_dir):
    return data_dir / "objs"

@pytest.fixture
def text_objs_dir(data_dir):
    return data_dir / "text_objs"

def test_path(text_objs_dir):
    assert BaseConfigObj() is not None
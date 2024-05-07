
import pytest, os

import sqlalchemy as sql
from app.db import orm

@pytest.fixture(scope="module")
def db_name():
    return "tests/test.db"

@pytest.fixture(scope="module")
def engine(db_name):
    e = sql.create_engine(f"sqlite:///{db_name}")
    yield e
    os.remove(db_name)

@pytest.fixture
def conn(engine):
    with engine.connect() as c:
        yield c
        
class Test_ORM:
    
    def test_init(self, conn):
        pass